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
Standard configuration files with `key = value` format that SliceBeam can import directly.

### .orca_printer Files  
JSON-based printer definition files with metadata that provide additional context to SliceBeam.

## How to Use with SliceBeam

1. **Download the profiles** to your Android device or cloud storage
2. **Open SliceBeam** on your Android device
3. **Import profiles**:
   - Go to Settings → Import Printer Profile
   - Select the desired profile file (.ini or .orca_printer)
   - The printer configuration will be imported and available for use

## Profile Features

These profiles include all the essential settings for the Bambu Lab A1 mini:

- **Print bed dimensions**: 180×180×180mm
- **Nozzle specifications** for each variant (0.2, 0.4, 0.6, 0.8mm)
- **Temperature settings** optimized for various filament types
- **Start/end G-code** specific to the A1 mini
- **Machine limits** (speeds, accelerations, etc.)
- **Retraction settings** tuned for the A1 mini's direct drive extruder
- **Bed leveling and calibration** routines

## Compatibility

- **Generated from**: OrcaSlicer profiles (latest version)
- **Compatible with**: SliceBeam Android app
- **Printer**: Bambu Lab A1 mini (all nozzle variants)
- **Date exported**: $(date +%Y-%m-%d)

## Notes

- Choose the profile that matches your installed nozzle size
- The 0.4mm nozzle is the most commonly used and recommended for general printing
- Smaller nozzles (0.2mm) provide higher detail but slower printing
- Larger nozzles (0.6mm, 0.8mm) allow faster printing with thicker layers

## Support

If you encounter issues with these profiles:

1. Ensure you're using the correct nozzle size profile
2. Verify your SliceBeam app is updated to the latest version
3. Check that your A1 mini firmware is current

## Credits

Profiles exported from OrcaSlicer using the `export_for_slicebeam.py` tool.