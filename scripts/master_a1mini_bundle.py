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
        
        # Find printer profiles (all nozzle sizes)
        vendor_dir = self.profiles_base_path / self.vendor
        machine_dir = vendor_dir / "machine"
        
        if machine_dir.exists():
            for json_file in machine_dir.glob("*A1*mini*.json"):
                profile = self.converter.load_profile_json(json_file)
                if profile.get("instantiation") == "true":
                    name = profile.get("name", json_file.stem)
                    # Include all 4 nozzle sizes
                    if any(size in name for size in ['0.2 nozzle', '0.4 nozzle', '0.6 nozzle', '0.8 nozzle']):
                        profiles["printer"].append(name)
        
        # Find key filament profiles
        filament_dir = vendor_dir / "filament"
        if filament_dir.exists():
            key_filaments = []
            
            # All major Bambu Lab filaments for A1M (avoid nozzle-specific variants)
            for json_file in filament_dir.glob("*A1M*.json"):
                profile = self.converter.load_profile_json(json_file)
                if profile.get("instantiation") == "true":
                    name = profile.get("name", json_file.stem)
                    # Include all major Bambu Lab materials, but avoid nozzle-specific variants
                    if any(material in name for material in [
                        'PLA Basic', 'PLA Silk', 'PLA Matte', 'PLA Tough', 'PLA Metal', 'PLA Marble',
                        'PLA Glow', 'PLA Dynamic', 'PLA Galaxy', 'PLA Sparkle', 'PLA Wood', 'PLA Aero',
                        'PETG Basic', 'PETG HF', 'PETG Translucent', 'PETG-CF',
                        'ABS @BBL A1M', 'ASA @BBL A1M',
                        'TPU 95A @BBL A1M', 'TPU for AMS @BBL A1M',
                        'Support For PLA @BBL A1M', 'Support For PLA-PETG @BBL A1M', 'Support W @BBL A1M',
                        'PVA @BBL A1M'
                    ]) and 'nozzle' not in name:
                        key_filaments.append(name)
                        
            # Add comprehensive A1 filaments (compatible with A1M)
            for json_file in filament_dir.glob("*A1.json"):
                if "A1M" not in json_file.name:
                    profile = self.converter.load_profile_json(json_file)
                    if profile.get("instantiation") == "true":
                        name = profile.get("name", json_file.stem)
                        # Include all Generic materials for A1 
                        if any(material in name for material in [
                            'Generic PLA @BBL A1', 'Generic PLA High Speed @BBL A1',
                            'Generic PETG @BBL A1', 'Generic PETG HF @BBL A1',
                            'Generic ABS @BBL A1', 'Generic ASA @BBL A1',
                            'Generic TPU @BBL A1', 'Generic TPU for AMS @BBL A1',
                            'Generic PC @BBL A1', 'Generic HIPS @BBL A1',
                            'Generic PVA @BBL A1'
                        ]):
                            key_filaments.append(name)
                            
            profiles["filament"] = sorted(list(set(key_filaments)))
        
        # Find key process profiles (including nozzle-specific variants)
        process_dir = vendor_dir / "process"
        if process_dir.exists():
            key_processes = []
            for json_file in process_dir.glob("*A1M*.json"):
                profile = self.converter.load_profile_json(json_file)
                if profile.get("instantiation") == "true":
                    name = profile.get("name", json_file.stem)
                    # Include key quality levels with and without nozzle variants
                    if any(quality in name for quality in [
                        # Standard quality levels (no nozzle specific)
                        '0.08mm High Quality @BBL A1M',
                        '0.08mm Extra Fine @BBL A1M',
                        '0.12mm Fine @BBL A1M',
                        '0.16mm High Quality @BBL A1M',
                        '0.16mm Optimal @BBL A1M', 
                        '0.20mm Standard @BBL A1M',
                        '0.20mm Strength @BBL A1M',
                        '0.24mm Draft @BBL A1M',
                        '0.28mm Extra Draft @BBL A1M',
                        # Nozzle-specific variants for fine printing
                        '0.06mm Fine @BBL A1M 0.2 nozzle',
                        '0.06mm High Quality @BBL A1M 0.2 nozzle',
                        '0.08mm High Quality @BBL A1M 0.2 nozzle',
                        '0.10mm High Quality @BBL A1M 0.2 nozzle',
                        '0.10mm Standard @BBL A1M 0.2 nozzle',
                        # Nozzle-specific variants for larger nozzles
                        '0.18mm Fine @BBL A1M 0.6 nozzle',
                        '0.24mm Optimal @BBL A1M 0.6 nozzle',
                        '0.30mm Standard @BBL A1M 0.6 nozzle',
                        '0.36mm Draft @BBL A1M 0.6 nozzle',
                        '0.24mm Fine @BBL A1M 0.8 nozzle',
                        '0.32mm Optimal @BBL A1M 0.8 nozzle',
                        '0.40mm Standard @BBL A1M 0.8 nozzle',
                        '0.48mm Draft @BBL A1M 0.8 nozzle'
                    ]):
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
        
    def create_master_bundle(self):
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
        for p in profiles['process'][:10]: 
            print(f"    - {p}")
        if len(profiles['process']) > 10:
            print(f"    - ... and {len(profiles['process'])-10} more")
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
            # Use 0.20mm Standard as default (good balance)
            default_process = None
            for process in profiles["process"]:
                if "0.20mm Standard @BBL A1M" in process and "nozzle" not in process:
                    default_process = process
                    break
            if not default_process and profiles["process"]:
                default_process = profiles["process"][len(profiles["process"])//2]  # Use middle option
            if default_process:
                bundle_lines.append(f"print = {default_process}")
                
        if profiles["printer"]:
            # Use 0.4mm as default (most common)
            default_printer = None
            for printer in profiles["printer"]:
                if "0.4 nozzle" in printer:
                    default_printer = printer
                    break
            if not default_printer:
                default_printer = profiles["printer"][0]
            bundle_lines.append(f"printer = {default_printer}")
            
        if profiles["filament"]:
            # Use PLA Basic as default (most common)
            default_filament = None
            for filament in profiles["filament"]:
                if "PLA Basic @BBL A1M" in filament:
                    default_filament = filament
                    break
            if not default_filament:
                default_filament = profiles["filament"][0]
            bundle_lines.append(f'filament = "{default_filament}"')
        
        return "\n".join(bundle_lines), profiles


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
    
    bundle_content, profile_counts = generator.create_master_bundle()
    if bundle_content:
        output_path = Path(args.output)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(bundle_content)
        print(f"✓ Successfully generated master bundle: {output_path}")
        print()
        print("This bundle contains:")
        print(f"- {len(profile_counts['printer'])} printer variants (all A1 mini nozzle sizes)")  
        print(f"- {len(profile_counts['filament'])} filament profiles (All Bambu Lab + Generic materials)")
        print(f"- {len(profile_counts['process'])} print quality profiles (including nozzle-specific variants)")
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