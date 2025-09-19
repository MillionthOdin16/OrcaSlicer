# Bambu Lab A1 mini Profiles for SliceBeam

This directory contains exported printer profiles for the **Bambu Lab A1 mini** 3D printer, formatted for use with the SliceBeam Android app.

## Included Profiles

The following nozzle variants are included:

| Nozzle Size | INI File | ORCA_PRINTER File |
|-------------|----------|-------------------|
| 0.2mm | `Bambu_Lab_A1_mini_02_nozzle.ini` | `Bambu_Lab_A1_mini_02_nozzle.orca_printer` |
| 0.4mm | `Bambu_Lab_A1_mini_04_nozzle.ini` | `Bambu_Lab_A1_mini_04_nozzle.orca_printer` |
| 0.6mm | `Bambu_Lab_A1_mini_06_nozzle.ini` | `Bambu_Lab_A1_mini_06_nozzle.orca_printer` |
| 0.8mm | `Bambu_Lab_A1_mini_08_nozzle.ini` | `Bambu_Lab_A1_mini_08_nozzle.orca_printer` |

## File Formats

### .ini Files
Complete SliceBeam configuration bundles with sections for:
- **[printer:...]** - A1 mini printer settings (bed size, speeds, G-code, etc.)
- **[print:...]** - Print profile with layer heights, speeds, and quality settings
- **[filament:...]** - Generic PLA filament profile with temperatures and cooling
- **[presets]** - Links all sections together for SliceBeam

These bundles contain everything needed for SliceBeam to import a complete printing configuration.

### .orca_printer Files  
JSON-based printer definition files with metadata that provide additional context to SliceBeam.

## How to Use with SliceBeam

1. **Download the profiles** to your Android device or cloud storage
2. **Open SliceBeam** on your Android device
3. **Import profiles**:
   - Go to Settings → Import Printer Profile
   - Select the desired `.ini` file (recommended for complete setup)
   - The complete printer configuration will be imported and available for use

## Profile Features

These profiles include all the essential settings for the Bambu Lab A1 mini:

- **Print bed dimensions**: 180×180×180mm
- **Nozzle specifications** for each variant (0.2, 0.4, 0.6, 0.8mm)
- **Temperature settings** optimized for PLA filament
- **Start/end G-code** specific to the A1 mini
- **Machine limits** (speeds, accelerations, etc.)
- **Retraction settings** tuned for the A1 mini's direct drive extruder
- **Bed leveling and calibration** routines
- **Complete print profiles** with quality settings

## Compatibility

- **Generated from**: OrcaSlicer profiles (latest version)
- **Compatible with**: SliceBeam Android app
- **Printer**: Bambu Lab A1 mini (all nozzle variants)
- **Date exported**: September 2024
- **Format**: SliceBeam config bundle format

## Notes

- **Recommended**: Use the `.ini` files for complete SliceBeam setup
- Choose the profile that matches your installed nozzle size
- The 0.4mm nozzle is the most commonly used and recommended for general printing
- Smaller nozzles (0.2mm) provide higher detail but slower printing
- Larger nozzles (0.6mm, 0.8mm) allow faster printing with thicker layers
- All profiles include PLA filament settings by default

## Recent Updates

**v2.0 (September 2024)**:
- ✅ **Fixed SliceBeam compatibility**: Profiles now use proper config bundle format
- ✅ **Complete printer setup**: Each `.ini` file includes printer, print, and filament settings
- ✅ **Tested format**: Compatible with SliceBeam's expected section structure
- ✅ **No more crashes**: Resolved import issues reported by users

## Support

If you encounter issues with these profiles:

1. Ensure you're using the `.ini` files (not `.orca_printer` for basic setup)
2. Verify your SliceBeam app is updated to the latest version
3. Check that your A1 mini firmware is current
4. Try importing one profile at a time

## Credits

Profiles exported from OrcaSlicer using the updated `export_for_slicebeam.py` tool with proper SliceBeam config bundle format.