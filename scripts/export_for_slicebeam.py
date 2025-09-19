#!/usr/bin/env python3
"""
OrcaSlicer Profile Export Tool for SliceBeam

This script provides a comprehensive way to export OrcaSlicer printer profiles
in formats compatible with the Android SliceBeam app.

Features:
- Export to .ini format (standard configuration file)
- Export to .orca_printer format (JSON-based printer definition)
- Batch export all profiles for a vendor
- Resolve inheritance chains automatically
- Generate ready-to-use profiles for SliceBeam

Usage Examples:
    # List available vendors
    python export_for_slicebeam.py --list-vendors
    
    # List profiles for a specific vendor
    python export_for_slicebeam.py --vendor "BBL" --list-profiles
    
    # Export single profile in both formats
    python export_for_slicebeam.py --vendor "BBL" --profile "Bambu Lab X1 Carbon 0.4 nozzle" --output-dir ./exports
    
    # Batch export all Bambu Lab profiles
    python export_for_slicebeam.py --vendor "BBL" --batch --output-dir ./bambu_exports
    
    # Export only .ini files
    python export_for_slicebeam.py --vendor "BBL" --batch --output-dir ./exports --format ini
    
    # Export only .orca_printer files
    python export_for_slicebeam.py --vendor "BBL" --batch --output-dir ./exports --format orca_printer
"""

import os
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union
from orca_profile_to_ini import OrcaProfileConverter
from orca_to_printer_file import OrcaPrinterFileGenerator


class SliceBeamExporter:
    def __init__(self, profiles_base_path: str):
        self.ini_converter = OrcaProfileConverter(profiles_base_path)
        self.orca_generator = OrcaPrinterFileGenerator(profiles_base_path)
    
    def export_profile(self, vendor: str, profile_name: str, output_dir: Path, 
                      formats: List[str] = None) -> bool:
        """Export a single profile in the specified formats."""
        if formats is None:
            formats = ["ini", "orca_printer"]
            
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create safe filename
        safe_name = "".join(c for c in profile_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        success = True
        
        # Export INI format
        if "ini" in formats:
            ini_content = self.ini_converter.convert_profile(vendor, profile_name)
            if ini_content:
                ini_file = output_dir / f"{safe_name}.ini"
                with open(ini_file, 'w', encoding='utf-8') as f:
                    f.write(ini_content)
                print(f"✓ INI: {profile_name} -> {ini_file}")
            else:
                print(f"✗ Failed to generate INI for: {profile_name}")
                success = False
        
        # Export .orca_printer format
        if "orca_printer" in formats:
            orca_content = self.orca_generator.generate_orca_printer_file(vendor, profile_name)
            if orca_content:
                orca_file = output_dir / f"{safe_name}.orca_printer"
                with open(orca_file, 'w', encoding='utf-8') as f:
                    json.dump(orca_content, f, indent=2, ensure_ascii=False)
                print(f"✓ ORCA: {profile_name} -> {orca_file}")
            else:
                print(f"✗ Failed to generate .orca_printer for: {profile_name}")
                success = False
        
        return success
    
    def batch_export(self, vendor: str, output_dir: Path, formats: List[str] = None) -> Dict[str, int]:
        """Batch export all profiles for a vendor."""
        if formats is None:
            formats = ["ini", "orca_printer"]
            
        profiles = self.ini_converter.get_vendor_profiles(vendor)
        if not profiles:
            print(f"No instantiation profiles found for vendor '{vendor}'")
            return {"total": 0, "success": 0, "failed": 0}
        
        stats = {"total": len(profiles), "success": 0, "failed": 0}
        
        print(f"\nExporting {len(profiles)} profiles for {vendor}...")
        print("=" * 60)
        
        for profile_name in profiles:
            if self.export_profile(vendor, profile_name, output_dir, formats):
                stats["success"] += 1
            else:
                stats["failed"] += 1
        
        return stats


def list_vendors(profiles_path: str) -> List[str]:
    """List all available vendors."""
    vendors = []
    profiles_dir = Path(profiles_path)
    
    for item in profiles_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Check if vendor has any machine profiles
            machine_dir = item / "machine"
            if machine_dir.exists() and any(machine_dir.glob("*.json")):
                vendors.append(item.name)
    
    return sorted(vendors)


def main():
    parser = argparse.ArgumentParser(
        description="Export OrcaSlicer profiles for SliceBeam Android app",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Get the default profiles path relative to this script
    script_dir = Path(__file__).parent
    default_profiles_path = script_dir.parent / "resources" / "profiles"
    
    parser.add_argument(
        "--profiles-path", 
        default=str(default_profiles_path),
        help="Path to OrcaSlicer profiles directory"
    )
    
    parser.add_argument("--list-vendors", action="store_true", help="List all available vendors")
    
    parser.add_argument("--vendor", help="Vendor name (e.g., 'BBL', 'Prusa')")
    parser.add_argument("--list-profiles", action="store_true", help="List all profiles for the specified vendor")
    
    parser.add_argument("--profile", help="Specific profile name to export")
    parser.add_argument("--batch", action="store_true", help="Export all profiles for the vendor")
    
    parser.add_argument("--output-dir", required=False, help="Output directory for exported files")
    
    parser.add_argument(
        "--format", 
        choices=["ini", "orca_printer", "both"], 
        default="both",
        help="Export format (default: both)"
    )
    
    args = parser.parse_args()
    
    if not Path(args.profiles_path).exists():
        print(f"Error: Profiles path '{args.profiles_path}' does not exist")
        return 1
    
    # List vendors
    if args.list_vendors:
        vendors = list_vendors(args.profiles_path)
        print("Available vendors with printer profiles:")
        print("=" * 40)
        for vendor in vendors:
            exporter = SliceBeamExporter(args.profiles_path)
            profile_count = len(exporter.ini_converter.get_vendor_profiles(vendor))
            print(f"  {vendor:<20} ({profile_count} profiles)")
        return 0
    
    if not args.vendor:
        print("Error: --vendor is required (use --list-vendors to see available vendors)")
        return 1
    
    exporter = SliceBeamExporter(args.profiles_path)
    
    # List profiles for vendor
    if args.list_profiles:
        profiles = exporter.ini_converter.get_vendor_profiles(args.vendor)
        if not profiles:
            print(f"No instantiation profiles found for vendor '{args.vendor}'")
            return 1
            
        print(f"Available profiles for {args.vendor}:")
        print("=" * 40)
        for i, profile in enumerate(profiles, 1):
            print(f"  {i:2d}. {profile}")
        return 0
    
    # Determine formats to export
    formats = []
    if args.format == "both":
        formats = ["ini", "orca_printer"]
    else:
        formats = [args.format]
    
    # Determine output directory
    if not args.output_dir:
        if args.batch:
            args.output_dir = f"./{args.vendor}_profiles"
        else:
            args.output_dir = "./exported_profile"
    
    output_dir = Path(args.output_dir)
    
    # Single profile export
    if args.profile:
        print(f"Exporting profile: {args.profile}")
        print(f"Vendor: {args.vendor}")
        print(f"Formats: {', '.join(formats)}")
        print(f"Output: {output_dir}")
        print("-" * 40)
        
        success = exporter.export_profile(args.vendor, args.profile, output_dir, formats)
        if success:
            print(f"\n✓ Successfully exported '{args.profile}'")
            return 0
        else:
            print(f"\n✗ Failed to export '{args.profile}'")
            return 1
    
    # Batch export
    if args.batch:
        print(f"Batch exporting profiles for vendor: {args.vendor}")
        print(f"Formats: {', '.join(formats)}")
        print(f"Output directory: {output_dir}")
        
        stats = exporter.batch_export(args.vendor, output_dir, formats)
        
        print("\n" + "=" * 60)
        print("EXPORT SUMMARY")
        print("=" * 60)
        print(f"Total profiles: {stats['total']}")
        print(f"Successfully exported: {stats['success']}")
        print(f"Failed: {stats['failed']}")
        
        if stats['failed'] == 0:
            print(f"\n✓ All profiles exported successfully to {output_dir}")
            print(f"\nTo use with SliceBeam:")
            print(f"1. Copy the .ini or .orca_printer files to your Android device")
            print(f"2. In SliceBeam, go to Settings > Import Printer Profile")
            print(f"3. Select the exported file to import the printer configuration")
            return 0
        else:
            print(f"\n⚠ Some profiles failed to export. Check output above for details.")
            return 1
    
    # If we get here, user didn't specify --profile or --batch
    print("Error: Specify either --profile <name> for single export or --batch for all profiles")
    print("Use --list-profiles to see available profiles for the vendor")
    return 1


if __name__ == "__main__":
    sys.exit(main())