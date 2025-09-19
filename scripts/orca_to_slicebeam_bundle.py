#!/usr/bin/env python3
"""
OrcaSlicer to SliceBeam Config Bundle Converter

This script creates complete config bundles for SliceBeam that include
printer, print profile, and filament settings in the proper INI format
with sections that SliceBeam expects.

Usage:
    python orca_to_slicebeam_bundle.py --vendor "BBL" --profile "Bambu Lab A1 mini 0.4 nozzle" --output bundle.ini
"""

import os
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union
from orca_profile_to_ini import OrcaProfileConverter


class SliceBeamBundleGenerator:
    def __init__(self, profiles_base_path: str):
        self.profiles_base_path = Path(profiles_base_path)
        self.converter = OrcaProfileConverter(profiles_base_path)
        
    def get_default_print_profile(self, vendor: str) -> Dict:
        """Get a basic print profile with sensible defaults."""
        return {
            "layer_height": "0.2",
            "first_layer_height": "0.2",
            "perimeters": "2",
            "top_solid_layers": "5", 
            "bottom_solid_layers": "5",
            "fill_density": "15%",
            "fill_pattern": "grid",
            "support_material": "0",
            "support_material_auto": "1",
            "support_material_threshold": "0",
            "bridge_speed": "25",
            "external_perimeter_speed": "50%",
            "infill_speed": "80",
            "perimeter_speed": "60",
            "small_perimeter_speed": "15",
            "solid_infill_speed": "20",
            "top_solid_infill_speed": "15",
            "travel_speed": "120",
            "first_layer_speed": "30",
            "skirts": "1",
            "skirt_distance": "6",
            "skirt_height": "1",
            "brim_width": "0",
            "solid_infill_extrusion_width": "0",
            "extrusion_width": "0",
            "first_layer_extrusion_width": "0",
            "perimeter_extrusion_width": "0",
            "external_perimeter_extrusion_width": "0",
            "infill_extrusion_width": "0",
            "support_material_extrusion_width": "0",
            "retract_length": "0.8",
            "retract_speed": "40",
            "retract_restart_extra": "0",
            "retract_before_travel": "2",
            "retract_lift": "0",
            "retract_lift_above": "0",
            "retract_lift_below": "0",
            "wipe": "0",
            "retract_before_wipe": "0%"
        }
        
    def get_default_filament_profile(self, vendor: str) -> Dict:
        """Get a basic PLA filament profile."""
        return {
            "filament_colour": "#29B2B2",
            "filament_diameter": "1.75",
            "filament_type": "PLA",
            "filament_density": "1.24",
            "filament_cost": "20",
            "temperature": "210",
            "first_layer_temperature": "210", 
            "bed_temperature": "60",
            "first_layer_bed_temperature": "60",
            "fan_always_on": "1",
            "cooling": "1",
            "min_fan_speed": "35",
            "max_fan_speed": "100",
            "bridge_fan_speed": "100",
            "disable_fan_first_layers": "3",
            "fan_below_layer_time": "60",
            "slowdown_below_layer_time": "5",
            "min_print_speed": "10",
            "max_print_speed": "80",
            "max_volumetric_speed": "0"
        }
        
    def convert_value_to_ini(self, value) -> str:
        """Convert a value to INI format string."""
        if isinstance(value, bool):
            return "1" if value else "0"
        elif isinstance(value, list):
            return ";".join(str(v) for v in value)
        elif value is None:
            return ""
        else:
            return str(value)
            
    def profile_dict_to_ini_section(self, profile_dict: Dict, skip_keys: set = None) -> List[str]:
        """Convert a profile dictionary to INI section lines."""
        if skip_keys is None:
            skip_keys = set()
            
        lines = []
        for key, value in sorted(profile_dict.items()):
            if key not in skip_keys:
                ini_value = self.convert_value_to_ini(value)
                lines.append(f"{key} = {ini_value}")
        return lines
        
    def generate_bundle(self, vendor: str, profile_name: str) -> Optional[str]:
        """Generate a complete SliceBeam config bundle."""
        
        # Get the printer profile
        profile_file = self.converter.find_profile_file(vendor, profile_name)
        if not profile_file:
            print(f"Error: Profile '{profile_name}' not found in vendor '{vendor}'")
            return None
            
        profile = self.converter.load_profile_json(profile_file)
        if not profile:
            return None
            
        # Resolve inheritance chain for printer
        resolved_printer = self.converter.resolve_inheritance(profile, vendor)
        
        # Get default print and filament profiles
        print_profile = self.get_default_print_profile(vendor)
        filament_profile = self.get_default_filament_profile(vendor)
        
        # Override print settings with any from printer profile that are relevant
        print_relevant_keys = {
            "layer_height", "first_layer_height", "retract_length", "retract_speed",
            "travel_speed", "first_layer_speed", "external_perimeter_speed"
        }
        for key in print_relevant_keys:
            if key in resolved_printer:
                print_profile[key] = resolved_printer[key]
                
        # Build the config bundle
        bundle_lines = []
        
        # Header
        bundle_lines.append("# generated by OrcaSlicer SliceBeam Export Tool")
        bundle_lines.append("")
        
        # Printer section
        printer_section_name = f"printer:{profile_name}"
        bundle_lines.append(f"[{printer_section_name}]")
        
        # Skip keys that shouldn't be in printer section
        printer_skip_keys = {
            "type", "name", "inherits", "from", "instantiation", 
            "setting_id", "default_filament_profile", "default_print_profile",
            "upward_compatible_machine"
        }
        
        printer_lines = self.profile_dict_to_ini_section(resolved_printer, printer_skip_keys)
        bundle_lines.extend(printer_lines)
        bundle_lines.append("")
        
        # Print section  
        print_section_name = f"print:0.20mm NORMAL @{vendor}"
        bundle_lines.append(f"[{print_section_name}]")
        print_lines = self.profile_dict_to_ini_section(print_profile)
        bundle_lines.extend(print_lines)
        bundle_lines.append("")
        
        # Filament section
        filament_section_name = f'"Generic PLA @{vendor}"'
        bundle_lines.append(f"[filament:{filament_section_name}]")
        filament_lines = self.profile_dict_to_ini_section(filament_profile)
        bundle_lines.extend(filament_lines)
        bundle_lines.append("")
        
        # Presets section
        bundle_lines.append("[presets]")
        bundle_lines.append(f"print = {print_section_name.split(':')[1]}")
        bundle_lines.append(f"printer = {printer_section_name.split(':')[1]}")
        bundle_lines.append(f"filament = {filament_section_name}")
        
        return "\n".join(bundle_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Convert OrcaSlicer profiles to SliceBeam config bundles",
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
    
    parser.add_argument("--vendor", required=True, help="Vendor name (e.g., 'BBL')")
    parser.add_argument("--profile", required=True, help="Profile name to convert")
    parser.add_argument("--output", required=True, help="Output bundle file path")
    
    args = parser.parse_args()
    
    if not Path(args.profiles_path).exists():
        print(f"Error: Profiles path '{args.profiles_path}' does not exist")
        return 1
        
    generator = SliceBeamBundleGenerator(args.profiles_path)
    
    print(f"Generating SliceBeam bundle for: {args.profile}")
    print(f"Vendor: {args.vendor}")
    print(f"Output: {args.output}")
    print("-" * 50)
    
    bundle_content = generator.generate_bundle(args.vendor, args.profile)
    if bundle_content:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(bundle_content)
        print(f"✓ Successfully generated bundle: {output_path}")
        return 0
    else:
        print(f"✗ Failed to generate bundle for: {args.profile}")
        return 1


if __name__ == "__main__":
    sys.exit(main())