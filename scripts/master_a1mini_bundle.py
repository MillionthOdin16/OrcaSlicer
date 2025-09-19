#!/usr/bin/env python3
"""
Master A1 mini SliceBeam Bundle Generator

This script creates a single comprehensive config bundle for SliceBeam that includes
ALL A1 mini profiles: multiple printers, filaments, and print profiles in one file.

Usage:
    python master_a1mini_bundle.py --output master_a1mini_bundle.ini
"""

import os
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union
from orca_profile_to_ini import OrcaProfileConverter
from orca_to_slicebeam_bundle import SliceBeamBundleGenerator


class MasterA1MiniBundleGenerator:
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
        
        # Find printer profiles (key nozzle sizes)
        vendor_dir = self.profiles_base_path / self.vendor
        machine_dir = vendor_dir / "machine"
        
        if machine_dir.exists():
            for json_file in machine_dir.glob("*A1*mini*.json"):
                profile = self.converter.load_profile_json(json_file)
                if profile.get("instantiation") == "true":
                    name = profile.get("name", json_file.stem)
                    # Include key nozzle sizes
                    if any(size in name for size in ['0.2 nozzle', '0.4 nozzle']):
                        profiles["printer"].append(name)
        
        # Find key filament profiles
        filament_dir = vendor_dir / "filament"
        if filament_dir.exists():
            key_filaments = []
            
            # Priority filaments for A1M (avoid nozzle-specific variants)
            for json_file in filament_dir.glob("*A1M*.json"):
                profile = self.converter.load_profile_json(json_file)
                if profile.get("instantiation") == "true":
                    name = profile.get("name", json_file.stem)
                    # Include most common materials, but avoid nozzle-specific variants
                    if any(material in name for material in [
                        'PLA Basic', 'PLA Silk', 'PLA Matte', 
                        'PETG Basic', 'PETG HF',
                        'ABS @BBL A1M',
                        'TPU 95A @BBL A1M'
                    ]) and 'nozzle' not in name:
                        key_filaments.append(name)
                        
            # Add some key A1 filaments (compatible with A1M)
            for json_file in filament_dir.glob("*A1.json"):
                if "A1M" not in json_file.name:
                    profile = self.converter.load_profile_json(json_file)
                    if profile.get("instantiation") == "true":
                        name = profile.get("name", json_file.stem)
                        if any(material in name for material in [
                            'Generic PLA @BBL A1',
                            'Generic PETG @BBL A1',
                            'Generic ABS @BBL A1'
                        ]):
                            key_filaments.append(name)
                            
            profiles["filament"] = sorted(list(set(key_filaments)))
        
        # Find key process profiles
        process_dir = vendor_dir / "process"
        if process_dir.exists():
            key_processes = []
            for json_file in process_dir.glob("*A1M*.json"):
                profile = self.converter.load_profile_json(json_file)
                if profile.get("instantiation") == "true":
                    name = profile.get("name", json_file.stem)
                    # Include key quality levels without nozzle-specific variants
                    if any(quality in name for quality in [
                        '0.08mm High Quality @BBL A1M',
                        '0.12mm Fine @BBL A1M',
                        '0.16mm Optimal @BBL A1M', 
                        '0.20mm Standard @BBL A1M',
                        '0.24mm Draft @BBL A1M'
                    ]) and 'nozzle' not in name:
                        key_processes.append(name)
                        
            profiles["process"] = sorted(list(set(key_processes)))
            
        return profiles
            
    def find_profile_file_comprehensive(self, vendor: str, profile_name: str) -> Optional[Path]:
        """Find the JSON file for a given profile name in any subdirectory."""
        vendor_dir = self.profiles_base_path / vendor
        if not vendor_dir.exists():
            return None
            
        # Check all subdirectories
        for subdir in ["machine", "filament", "process"]:
            dir_path = vendor_dir / subdir
            if dir_path.exists():
                for json_file in dir_path.glob("*.json"):
                    profile = self.converter.load_profile_json(json_file)
                    if profile.get("name") == profile_name:
                        return json_file
        
        # Check root vendor directory
        for json_file in vendor_dir.glob("*.json"):
            profile = self.converter.load_profile_json(json_file)
            if profile.get("name") == profile_name:
                return json_file
                
        return None
        
    def create_master_bundle(self) -> Optional[str]:
        """Create a master config bundle with all A1 mini profiles."""
        
        profiles = self.find_a1mini_profiles()
        
        print(f"Creating master bundle with:")
        print(f"  Printers: {len(profiles['printer'])}")
        for p in profiles['printer']: 
            print(f"    - {p}")
        print(f"  Filaments: {len(profiles['filament'])}")
        for f in profiles['filament'][:5]: 
            print(f"    - {f}")
        if len(profiles['filament']) > 5:
            print(f"    - ... and {len(profiles['filament'])-5} more")
        print(f"  Processes: {len(profiles['process'])}")
        for p in profiles['process']: 
            print(f"    - {p}")
        print()
        
        bundle_lines = []
        
        # Header
        bundle_lines.append("# Master A1 mini Bundle for SliceBeam")
        bundle_lines.append("# Contains all key printer, filament, and print profiles")
        bundle_lines.append("# Generated by OrcaSlicer Master Bundle Export Tool")
        bundle_lines.append("")
        
        # Add all printer sections
        for printer_name in profiles["printer"]:
            printer_file = self.find_profile_file_comprehensive(self.vendor, printer_name)
            if not printer_file:
                continue
                
            printer_profile = self.converter.load_profile_json(printer_file)
            if not printer_profile:
                continue
                
            resolved_printer = self.converter.resolve_inheritance(printer_profile, self.vendor)
            
            # Printer section
            bundle_lines.append(f"[printer:{printer_name}]")
            
            printer_skip_keys = {
                "type", "name", "inherits", "from", "instantiation", 
                "setting_id", "default_filament_profile", "default_print_profile",
                "upward_compatible_machine"
            }
            
            printer_lines = self.bundle_generator.profile_dict_to_ini_section(resolved_printer, printer_skip_keys)
            bundle_lines.extend(printer_lines)
            bundle_lines.append("")
            
        # Add all print/process sections
        for process_name in profiles["process"]:
            print(f"Processing print profile: {process_name}")
            process_file = self.find_profile_file_comprehensive(self.vendor, process_name)
            if not process_file:
                print(f"  Could not find process file for: {process_name}")
                continue
                
            process_profile = self.converter.load_profile_json(process_file)
            if not process_profile:
                print(f"  Could not load process profile for: {process_name}")
                continue
                
            resolved_process = self.converter.resolve_inheritance(process_profile, self.vendor)
            
            # Process section
            bundle_lines.append(f"[print:{process_name}]")
            
            process_skip_keys = {
                "type", "name", "inherits", "from", "instantiation", 
                "setting_id", "compatible_printers", "compatible_printers_condition"
            }
            
            process_lines = self.bundle_generator.profile_dict_to_ini_section(resolved_process, process_skip_keys)
            bundle_lines.extend(process_lines)
            bundle_lines.append("")
            print(f"  Added process section with {len(process_lines)} lines")
            
        # Add all filament sections
        for filament_name in profiles["filament"]:
            print(f"Processing filament profile: {filament_name}")
            filament_file = self.find_profile_file_comprehensive(self.vendor, filament_name)
            if not filament_file:
                print(f"  Could not find filament file for: {filament_name}")
                continue
                
            filament_profile = self.converter.load_profile_json(filament_file)
            if not filament_profile:
                print(f"  Could not load filament profile for: {filament_name}")
                continue
                
            resolved_filament = self.converter.resolve_inheritance(filament_profile, self.vendor)
            
            # Filament section
            bundle_lines.append(f'[filament:"{filament_name}"]')
            
            filament_skip_keys = {
                "type", "name", "inherits", "from", "instantiation", 
                "setting_id", "compatible_printers", "compatible_printers_condition",
                "compatible_prints", "compatible_prints_condition"
            }
            
            filament_lines = self.bundle_generator.profile_dict_to_ini_section(resolved_filament, filament_skip_keys)
            bundle_lines.extend(filament_lines)
            bundle_lines.append("")
            print(f"  Added filament section with {len(filament_lines)} lines")
            
        # Presets section with defaults
        bundle_lines.append("[presets]")
        if profiles["process"]:
            bundle_lines.append(f"print = {profiles['process'][2]}")  # Use 0.16mm Optimal as default
        if profiles["printer"]:
            bundle_lines.append(f"printer = {profiles['printer'][1]}")  # Use 0.4mm as default
        if profiles["filament"]:
            bundle_lines.append(f'filament = "{profiles["filament"][0]}"')  # Use first filament as default
        
        return "\n".join(bundle_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Create master A1 mini SliceBeam bundle with all profiles",
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
        "--output", 
        default="master_a1mini_slicebeam_bundle.ini",
        help="Output master bundle file"
    )
    
    args = parser.parse_args()
    
    if not Path(args.profiles_path).exists():
        print(f"Error: Profiles path '{args.profiles_path}' does not exist")
        return 1
        
    generator = MasterA1MiniBundleGenerator(args.profiles_path)
    
    print("Master Bambu Lab A1 mini SliceBeam Bundle Generator")
    print("=" * 55)
    print(f"Output: {args.output}")
    print()
    
    bundle_content = generator.create_master_bundle()
    if bundle_content:
        output_path = Path(args.output)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(bundle_content)
        print(f"✓ Successfully generated master bundle: {output_path}")
        print()
        print("This bundle contains:")
        print("- 2 printer variants (0.2mm and 0.4mm nozzles)")  
        print("- 8+ key filament profiles (PLA, PETG, ABS, TPU, Generic)")
        print("- 5 print quality levels (0.08mm to 0.24mm)")
        print()
        print("To use with SliceBeam:")
        print("1. Copy this single .ini file to your Android device")
        print("2. In SliceBeam: Settings → Import Printer Profile")
        print("3. Import this file once to get ALL A1 mini profiles")
        print("4. Switch between different combinations in SliceBeam settings")
        return 0
    else:
        print(f"✗ Failed to generate master bundle")
        return 1


if __name__ == "__main__":
    sys.exit(main())