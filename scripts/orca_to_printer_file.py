#!/usr/bin/env python3
"""
OrcaSlicer Profile to .orca_printer Converter

This script creates .orca_printer files that can be imported into SliceBeam.
The .orca_printer format appears to be a JSON-based format that bundles
the printer configuration with metadata.

Usage:
    python orca_to_printer_file.py --vendor "BBL" --profile "Bambu Lab X1 Carbon 0.4 nozzle" --output x1c.orca_printer
"""

import os
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union
from orca_profile_to_ini import OrcaProfileConverter


class OrcaPrinterFileGenerator:
    def __init__(self, profiles_base_path: str):
        self.converter = OrcaProfileConverter(profiles_base_path)
    
    def generate_orca_printer_file(self, vendor: str, profile_name: str) -> Optional[Dict]:
        """Generate .orca_printer file content."""
        profile_file = self.converter.find_profile_file(vendor, profile_name)
        if not profile_file:
            print(f"Error: Profile '{profile_name}' not found in vendor '{vendor}'")
            return None
            
        profile = self.converter.load_profile_json(profile_file)
        if not profile:
            return None
            
        # Resolve inheritance chain
        resolved_profile = self.converter.resolve_inheritance(profile, vendor)
        
        # Create the .orca_printer file structure
        orca_printer = {
            "version": "1.0.0",
            "type": "printer",
            "name": resolved_profile.get("name", profile_name),
            "vendor": vendor,
            "printer_model": resolved_profile.get("printer_model", ""),
            "printer_variant": resolved_profile.get("printer_variant", ""),
            "nozzle_diameter": resolved_profile.get("nozzle_diameter", ["0.4"]),
            "printer_technology": "FFF",
            "config": {}
        }
        
        # Skip metadata fields that aren't printer settings
        skip_keys = {
            "type", "name", "inherits", "from", "instantiation", 
            "setting_id", "default_filament_profile", "default_print_profile",
            "upward_compatible_machine", "printer_model", "printer_variant"
        }
        
        # Copy configuration parameters
        for key, value in resolved_profile.items():
            if key not in skip_keys:
                orca_printer["config"][key] = value
        
        return orca_printer


def main():
    parser = argparse.ArgumentParser(
        description="Convert OrcaSlicer JSON profiles to .orca_printer format for SliceBeam",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Convert single profile:
    python orca_to_printer_file.py --vendor "BBL" --profile "Bambu Lab X1 Carbon 0.4 nozzle" --output x1c.orca_printer
    
  Convert all profiles for a vendor:
    python orca_to_printer_file.py --vendor "BBL" --batch --output-dir ./exported
        """
    )
    
    # Get the default profiles path relative to this script
    script_dir = Path(__file__).parent
    default_profiles_path = script_dir.parent / "resources" / "profiles"
    
    parser.add_argument(
        "--profiles-path", 
        default=str(default_profiles_path),
        help="Path to OrcaSlicer profiles directory"
    )
    
    parser.add_argument("--vendor", required=True, help="Vendor name (e.g., 'BBL', 'Prusa')")
    parser.add_argument("--profile", help="Profile name to convert")
    parser.add_argument("--output", help="Output .orca_printer file path")
    
    parser.add_argument("--batch", action="store_true", help="Convert all profiles for the vendor")
    parser.add_argument("--output-dir", help="Output directory for batch conversion")
    
    args = parser.parse_args()
    
    if not Path(args.profiles_path).exists():
        print(f"Error: Profiles path '{args.profiles_path}' does not exist")
        return 1
    
    generator = OrcaPrinterFileGenerator(args.profiles_path)
    
    # Batch conversion
    if args.batch:
        if not args.output_dir:
            print("Error: --output-dir is required for batch conversion")
            return 1
            
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        profiles = generator.converter.get_vendor_profiles(args.vendor)
        if not profiles:
            print(f"No instantiation profiles found for vendor '{args.vendor}'")
            return 1
            
        for profile_name in profiles:
            orca_printer_content = generator.generate_orca_printer_file(args.vendor, profile_name)
            if orca_printer_content:
                # Create safe filename
                safe_name = "".join(c for c in profile_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_name = safe_name.replace(' ', '_')
                output_file = output_dir / f"{safe_name}.orca_printer"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(orca_printer_content, f, indent=2, ensure_ascii=False)
                print(f"Converted: {profile_name} -> {output_file}")
            else:
                print(f"Failed to convert: {profile_name}")
        
        return 0
    
    # Single profile conversion
    if not args.profile:
        print("Error: --profile is required for single conversion")
        return 1
        
    if not args.output:
        print("Error: --output is required for single conversion")
        return 1
    
    orca_printer_content = generator.generate_orca_printer_file(args.vendor, args.profile)
    if not orca_printer_content:
        return 1
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(orca_printer_content, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully converted '{args.profile}' to '{args.output}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())