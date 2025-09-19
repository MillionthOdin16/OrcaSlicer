# OrcaSlicer Profile Export for SliceBeam

This toolkit allows you to export OrcaSlicer printer profiles for use with the Android SliceBeam app without needing to run the OrcaSlicer application.

## Overview

SliceBeam is an Android app that can slice 3D models for printing. It supports importing printer profiles from OrcaSlicer but requires them in specific formats:
- `.ini` files (standard configuration format)
- `.orca_printer` files (JSON-based printer definition)

This toolkit converts OrcaSlicer's JSON profile format to these compatible formats, automatically resolving inheritance chains and flattening configurations.

## Features

- **Automatic inheritance resolution**: Profiles that inherit from other profiles are automatically merged
- **Multiple export formats**: Generate both .ini and .orca_printer files
- **Batch processing**: Export all profiles for a vendor at once
- **Comprehensive vendor support**: Works with all vendors in OrcaSlicer (Bambu Lab, Prusa, Creality, etc.)
- **Safe filename generation**: Automatically creates filesystem-safe filenames
- **Validation**: Only exports instantiation profiles (actual printer configurations, not templates)

## Installation & Requirements

### Prerequisites
- Python 3.6 or higher
- OrcaSlicer source code or profiles directory

### Setup
1. Clone or download the OrcaSlicer repository
2. Navigate to the `scripts` directory
3. The export tools are ready to use (no additional dependencies required)

## Usage

### Quick Start

```bash
# Navigate to OrcaSlicer directory
cd /path/to/OrcaSlicer

# List available vendors
python scripts/export_for_slicebeam.py --list-vendors

# List profiles for Bambu Lab
python scripts/export_for_slicebeam.py --vendor "BBL" --list-profiles

# Export a single printer profile
python scripts/export_for_slicebeam.py --vendor "BBL" --profile "Bambu Lab X1 Carbon 0.4 nozzle" --output-dir ./exports

# Export all Bambu Lab profiles
python scripts/export_for_slicebeam.py --vendor "BBL" --batch --output-dir ./bambu_exports
```

### Detailed Examples

#### 1. Export Single Profile (Both Formats)
```bash
python scripts/export_for_slicebeam.py \
    --vendor "BBL" \
    --profile "Bambu Lab X1 Carbon 0.4 nozzle" \
    --output-dir ./my_printer
```
This creates:
- `Bambu_Lab_X1_Carbon_04_nozzle.ini`
- `Bambu_Lab_X1_Carbon_04_nozzle.orca_printer`

#### 2. Export Only INI Files
```bash
python scripts/export_for_slicebeam.py \
    --vendor "Prusa" \
    --batch \
    --format ini \
    --output-dir ./prusa_ini_files
```

#### 3. Export Only .orca_printer Files
```bash
python scripts/export_for_slicebeam.py \
    --vendor "Creality" \
    --batch \
    --format orca_printer \
    --output-dir ./creality_orca_files
```

#### 4. Export All Vendors (Advanced)
```bash
# Create script to export all vendors
for vendor in $(python scripts/export_for_slicebeam.py --list-vendors | tail -n +3 | awk '{print $1}'); do
    echo "Exporting $vendor..."
    python scripts/export_for_slicebeam.py --vendor "$vendor" --batch --output-dir "./all_exports/$vendor"
done
```

### Command Reference

#### Main Export Tool (`export_for_slicebeam.py`)

```
python scripts/export_for_slicebeam.py [OPTIONS]

Options:
  --list-vendors          List all available vendors
  --vendor VENDOR         Vendor name (required for operations)
  --list-profiles         List profiles for the specified vendor
  --profile NAME          Export specific profile
  --batch                 Export all profiles for vendor
  --output-dir DIR        Output directory (auto-generated if not specified)
  --format FORMAT         Export format: ini, orca_printer, or both (default: both)
  --profiles-path PATH    Custom path to profiles directory
```

#### Individual Tools

For advanced use cases, you can also use the individual conversion tools:

```bash
# INI export only
python scripts/orca_profile_to_ini.py --vendor "BBL" --profile "Profile Name" --output file.ini

# .orca_printer export only  
python scripts/orca_to_printer_file.py --vendor "BBL" --profile "Profile Name" --output file.orca_printer
```

## Using Exported Profiles with SliceBeam

### Method 1: Transfer Files to Android Device

1. Export profiles using this toolkit
2. Copy the `.ini` or `.orca_printer` files to your Android device
3. In SliceBeam:
   - Go to Settings → Import Printer Profile
   - Select the exported file
   - The printer configuration will be imported and available for use

### Method 2: Cloud Storage

1. Export profiles to a cloud storage folder (Dropbox, Google Drive, etc.)
2. Access the files from your Android device
3. Import into SliceBeam as above

## Profile Structure & Compatibility

### Inheritance Resolution

OrcaSlicer profiles use inheritance where specific printer variants inherit settings from base profiles. For example:

```
fdm_machine_common.json (base settings for all FDM printers)
    ↓ inherits
fdm_bbl_3dp_001_common.json (Bambu Lab specific settings)
    ↓ inherits
Bambu Lab X1 Carbon 0.4 nozzle.json (specific printer variant)
```

This toolkit automatically resolves these inheritance chains, ensuring the exported profile contains all necessary settings.

### Exported Configuration Categories

The exported profiles include:

- **Machine limits**: Max speeds, accelerations, jerks
- **Print area**: Bed size, exclude areas, clearances  
- **Extruder settings**: Nozzle diameter, retraction, temperatures
- **G-code**: Start/end scripts, layer change scripts
- **Hardware features**: Auxiliary fans, chamber control, sensors
- **Filament handling**: AMS/multi-material settings

## File Formats

### .ini Format
Standard configuration file with `key = value` pairs:
```ini
# OrcaSlicer Profile: Bambu Lab X1 Carbon 0.4 nozzle
# Generated by orca_profile_to_ini.py

auxiliary_fan = 1
bed_exclude_area = 0x0;18x0;18x28;0x28
extruder_colour = #018001
machine_max_speed_x = 500;200
nozzle_diameter = 0.4
printer_technology = FFF
retraction_length = 0.8
...
```

### .orca_printer Format
JSON-based format with metadata and configuration:
```json
{
  "version": "1.0.0",
  "type": "printer",
  "name": "Bambu Lab X1 Carbon 0.4 nozzle",
  "vendor": "BBL",
  "printer_model": "Bambu Lab X1 Carbon",
  "printer_variant": "0.4",
  "nozzle_diameter": ["0.4"],
  "printer_technology": "FFF",
  "config": {
    "auxiliary_fan": "1",
    "bed_exclude_area": ["0x0", "18x0", "18x28", "0x28"],
    ...
  }
}
```

## Supported Vendors

The toolkit supports all vendors included in OrcaSlicer:

**Major Brands**: Bambu Lab (BBL), Prusa, Creality, Anycubic, Artillery, Elegoo, Flashforge, Qidi, Raise3D, Snapmaker, Ultimaker

**Specialty/Community**: Voron, Ratrig, Custom, OrcaArena, and many others

**Total**: 50+ vendors with 700+ printer profiles

## Troubleshooting

### Common Issues

**1. "Profile not found" error**
- Use `--list-profiles` to see exact profile names
- Profile names are case-sensitive
- Make sure you're using the correct vendor name

**2. "No instantiation profiles found"**
- The vendor exists but has no actual printer profiles (only templates)
- Check with `--list-profiles` to confirm

**3. Empty or incomplete profiles**
- Some profiles may have minimal settings and inherit everything from parents
- The inheritance resolution should handle this automatically

**4. Large G-code blocks in INI files**
- This is normal - start/end G-code can be quite large
- SliceBeam should handle this correctly

### Debug Mode

For troubleshooting, you can examine individual components:

```bash
# Check profile inheritance
python scripts/orca_profile_to_ini.py --vendor "BBL" --profile "Bambu Lab X1 Carbon 0.4 nozzle" --output debug.ini

# Examine the raw JSON profile
cat resources/profiles/BBL/machine/"Bambu Lab X1 Carbon 0.4 nozzle.json"
```

## Contributing

This toolkit is part of the OrcaSlicer project. To contribute:

1. Test with different vendors and profiles
2. Report issues with specific profiles that fail to convert
3. Suggest improvements for SliceBeam compatibility
4. Add support for additional export formats if needed

## License

This toolkit is distributed under the same license as OrcaSlicer.

## Changelog

- **v1.0**: Initial release with .ini and .orca_printer export support
- Automatic inheritance resolution
- Batch export capabilities
- Comprehensive vendor support