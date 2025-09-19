#!/usr/bin/env python3
"""
Comprehensive SliceBeam Bundle Exporter for A1 mini

This script creates complete config bundles for SliceBeam that include all
printer, filament, and print profiles for the Bambu Lab A1 mini.

Usage:
    python comprehensive_a1mini_export.py --output-dir ./a1mini_complete_export
"""

import os
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union
from orca_profile_to_ini import OrcaProfileConverter
from orca_to_slicebeam_bundle import SliceBeamBundleGenerator


class ComprehensiveA1MiniExporter:
    def __init__(self, profiles_base_path: str):
        self.profiles_base_path = Path(profiles_base_path)
        self.converter = OrcaProfileConverter(profiles_base_path)
        self.bundle_generator = SliceBeamBundleGenerator(profiles_base_path)
        self.vendor = "BBL"
        
    def find_a1mini_profiles(self) -> Dict[str, List[str]]:
        """Find all A1 mini related profiles."""
        profiles = {
            "printer": [],
            "filament": [],
            "process": []
        }
        
        # Find printer profiles
        vendor_dir = self.profiles_base_path / self.vendor
        machine_dir = vendor_dir / "machine"
        
        if machine_dir.exists():
            for json_file in machine_dir.glob("*A1*mini*.json"):
                profile = self.converter.load_profile_json(json_file)
                if profile.get("instantiation") == "true":
                    profiles["printer"].append(profile.get("name", json_file.stem))
        
        # Find filament profiles
        filament_dir = vendor_dir / "filament"
        if filament_dir.exists():
            for json_file in filament_dir.glob("*A1M*.json"):
                profile = self.converter.load_profile_json(json_file)
                if profile.get("instantiation") == "true":
                    profiles["filament"].append(profile.get("name", json_file.stem))
                    
            # Also include some key A1 (non-mini) filaments that work with A1M
            for json_file in filament_dir.glob("*A1.json"):
                if "A1M" not in json_file.name:  # Avoid duplicates
                    profile = self.converter.load_profile_json(json_file)
                    if profile.get("instantiation") == "true":
                        name = profile.get("name", json_file.stem)
                        if any(material in name for material in ["PLA", "PETG", "ABS", "TPU", "Generic"]):
                            profiles["filament"].append(name)
        
        # Find process profiles  
        process_dir = vendor_dir / "process"
        if process_dir.exists():
            for json_file in process_dir.glob("*A1M*.json"):
                profile = self.converter.load_profile_json(json_file)
                if profile.get("instantiation") == "true":
                    profiles["process"].append(profile.get("name", json_file.stem))
        
        # Remove duplicates and sort
        for key in profiles:
            profiles[key] = sorted(list(set(profiles[key])))
            
        return profiles
        
    def load_filament_profile(self, filament_name: str) -> Optional[Dict]:
        """Load and resolve a filament profile."""
        filament_file = self.converter.find_profile_file(self.vendor, filament_name)
        if not filament_file:
            return None
            
        profile = self.converter.load_profile_json(filament_file)
        if not profile:
            return None
            
        return self.converter.resolve_inheritance(profile, self.vendor)
        
    def load_process_profile(self, process_name: str) -> Optional[Dict]:
        """Load and resolve a process profile."""
        process_file = self.converter.find_profile_file(self.vendor, process_name)
        if not process_file:
            return None
            
        profile = self.converter.load_profile_json(process_file)
        if not profile:
            return None
            
        return self.converter.resolve_inheritance(profile, self.vendor)
        
    def create_comprehensive_bundle(self, printer_name: str, filament_name: str, 
                                  process_name: str) -> Optional[str]:
        """Create a comprehensive config bundle with specific printer, filament, and process."""
        
        # Get printer profile (reuse existing logic)
        printer_file = self.converter.find_profile_file(self.vendor, printer_name)
        if not printer_file:
            return None
            
        printer_profile = self.converter.load_profile_json(printer_file)
        if not printer_profile:
            return None
            
        resolved_printer = self.converter.resolve_inheritance(printer_profile, self.vendor)
        
        # Get filament profile
        filament_profile = self.load_filament_profile(filament_name)
        if not filament_profile:
            print(f"Warning: Could not load filament profile: {filament_name}")
            filament_profile = self.bundle_generator.get_default_filament_profile(self.vendor)
            
        # Get process profile  
        process_profile = self.load_process_profile(process_name)
        if not process_profile:
            print(f"Warning: Could not load process profile: {process_name}")
            process_profile = self.bundle_generator.get_default_print_profile(self.vendor)
            
        # Build the comprehensive config bundle
        bundle_lines = []
        
        # Header
        bundle_lines.append("# generated by OrcaSlicer Comprehensive A1 mini Export Tool")
        bundle_lines.append(f"# Printer: {printer_name}")
        bundle_lines.append(f"# Filament: {filament_name}")
        bundle_lines.append(f"# Process: {process_name}")
        bundle_lines.append("")
        
        # Printer section
        printer_section_name = f"printer:{printer_name}"
        bundle_lines.append(f"[{printer_section_name}]")
        
        printer_skip_keys = {
            "type", "name", "inherits", "from", "instantiation", 
            "setting_id", "default_filament_profile", "default_print_profile",
            "upward_compatible_machine"
        }
        
        printer_lines = self.bundle_generator.profile_dict_to_ini_section(resolved_printer, printer_skip_keys)
        bundle_lines.extend(printer_lines)
        bundle_lines.append("")
        
        # Print/Process section
        print_section_name = f"print:{process_name}"
        bundle_lines.append(f"[{print_section_name}]")
        
        process_skip_keys = {
            "type", "name", "inherits", "from", "instantiation", 
            "setting_id", "compatible_printers", "compatible_printers_condition"
        }
        
        process_lines = self.bundle_generator.profile_dict_to_ini_section(process_profile, process_skip_keys)
        bundle_lines.extend(process_lines)
        bundle_lines.append("")
        
        # Filament section
        filament_section_name = f'"{filament_name}"'
        bundle_lines.append(f"[filament:{filament_section_name}]")
        
        filament_skip_keys = {
            "type", "name", "inherits", "from", "instantiation", 
            "setting_id", "compatible_printers", "compatible_printers_condition",
            "compatible_prints", "compatible_prints_condition"
        }
        
        filament_lines = self.bundle_generator.profile_dict_to_ini_section(filament_profile, filament_skip_keys)
        bundle_lines.extend(filament_lines)
        bundle_lines.append("")
        
        # Presets section
        bundle_lines.append("[presets]")
        bundle_lines.append(f"print = {process_name}")
        bundle_lines.append(f"printer = {printer_name}")
        bundle_lines.append(f"filament = {filament_section_name}")
        
        return "\n".join(bundle_lines)
        
    def export_all_combinations(self, output_dir: Path, limit_combinations: bool = True):
        """Export comprehensive bundles for all meaningful combinations."""
        
        profiles = self.find_a1mini_profiles()
        
        print(f"Found profiles:")
        print(f"  Printers: {len(profiles['printer'])}")
        print(f"  Filaments: {len(profiles['filament'])}")
        print(f"  Processes: {len(profiles['process'])}")
        print()
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Select key combinations to avoid overwhelming number of files
        if limit_combinations:
            # Key printer profiles (most common nozzle sizes)
            key_printers = [p for p in profiles['printer'] if any(size in p for size in ['0.4 nozzle', '0.2 nozzle'])]
            
            # Key filament profiles (most popular materials)
            key_filaments = []
            for filament in profiles['filament']:
                if any(material in filament for material in [
                    'PLA Basic', 'PLA Silk', 'PETG Basic', 'ABS @BBL A1', 
                    'TPU 95A', 'Generic PLA', 'Generic PETG', 'Generic ABS'
                ]):
                    key_filaments.append(filament)
                    
            # Key process profiles (common layer heights)
            key_processes = []
            for process in profiles['process']:
                if any(quality in process for quality in [
                    '0.20mm Standard', '0.16mm Optimal', '0.12mm Fine', 
                    '0.24mm Draft', '0.08mm High Quality'
                ]):
                    key_processes.append(process)
                    
            profiles['printer'] = key_printers[:4]  # Limit to 4 printers
            profiles['filament'] = key_filaments[:15]  # Limit to 15 key filaments  
            profiles['process'] = key_processes[:8]   # Limit to 8 key processes
            
        successful = 0
        failed = 0
        
        print(f"Generating bundles for {len(profiles['printer'])} printers × {len(profiles['filament'])} filaments × {len(profiles['process'])} processes")
        print(f"Total combinations: {len(profiles['printer']) * len(profiles['filament']) * len(profiles['process'])}")
        print("=" * 80)
        
        for printer in profiles['printer']:
            for filament in profiles['filament'][:10]:  # Limit filaments per printer to keep manageable
                for process in profiles['process'][:5]:   # Limit processes per combination
                    
                    # Create safe filename
                    safe_printer = "".join(c for c in printer if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')
                    safe_filament = "".join(c for c in filament if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')
                    safe_process = "".join(c for c in process if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')
                    
                    filename = f"{safe_printer}--{safe_filament}--{safe_process}.ini"
                    
                    # Generate bundle
                    bundle_content = self.create_comprehensive_bundle(printer, filament, process)
                    if bundle_content:
                        bundle_file = output_dir / filename
                        with open(bundle_file, 'w', encoding='utf-8') as f:
                            f.write(bundle_content)
                        print(f"✓ {filename}")
                        successful += 1
                    else:
                        print(f"✗ Failed: {filename}")
                        failed += 1
                        
        print("=" * 80)
        print(f"Export Summary:")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"  Total: {successful + failed}")
        
        return successful, failed


def main():
    parser = argparse.ArgumentParser(
        description="Export comprehensive A1 mini profiles for SliceBeam",
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
    
    parser.add_argument(
        "--output-dir", 
        default="./a1mini_comprehensive_export",
        help="Output directory for comprehensive bundles"
    )
    
    parser.add_argument(
        "--full-export", 
        action="store_true",
        help="Export all combinations (warning: generates many files)"
    )
    
    args = parser.parse_args()
    
    if not Path(args.profiles_path).exists():
        print(f"Error: Profiles path '{args.profiles_path}' does not exist")
        return 1
        
    exporter = ComprehensiveA1MiniExporter(args.profiles_path)
    
    print("Comprehensive Bambu Lab A1 mini SliceBeam Export")
    print("=" * 50)
    print(f"Output directory: {args.output_dir}")
    print(f"Full export: {args.full_export}")
    print()
    
    output_dir = Path(args.output_dir)
    
    successful, failed = exporter.export_all_combinations(
        output_dir, 
        limit_combinations=not args.full_export
    )
    
    if successful > 0:
        print(f"\n✓ Successfully exported {successful} comprehensive config bundles!")
        print(f"\nTo use with SliceBeam:")
        print(f"1. Copy any .ini file to your Android device")
        print(f"2. In SliceBeam: Settings → Import Printer Profile")
        print(f"3. Select the bundle that matches your desired printer/filament/quality combination")
        print(f"4. Complete setup will be imported automatically")
        return 0
    else:
        print(f"\n✗ Export failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())