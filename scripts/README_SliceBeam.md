# SliceBeam Profile Export Scripts

This directory contains Python scripts to export OrcaSlicer printer profiles for use with the Android SliceBeam app.

## Quick Usage

```bash
# Export a single printer profile for SliceBeam
python export_for_slicebeam.py --vendor "BBL" --profile "Bambu Lab X1 Carbon 0.4 nozzle" --output-dir ./exports

# Export all profiles for a vendor
python export_for_slicebeam.py --vendor "BBL" --batch --output-dir ./bambu_exports

# List available vendors and profiles
python export_for_slicebeam.py --list-vendors
python export_for_slicebeam.py --vendor "BBL" --list-profiles
```

## Scripts

- **`export_for_slicebeam.py`** - Main tool for exporting profiles (recommended)
- **`orca_profile_to_ini.py`** - Convert profiles to .ini format
- **`orca_to_printer_file.py`** - Convert profiles to .orca_printer format

## Documentation

See `../docs/SliceBeam_Export_Guide.md` for complete documentation and usage examples.

## Output Formats

- **`.ini`** - Standard configuration format that SliceBeam can import
- **`.orca_printer`** - JSON-based printer definition format

Both formats are supported by SliceBeam for importing printer configurations.