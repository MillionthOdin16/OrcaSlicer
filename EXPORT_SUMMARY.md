# Bambu Lab A1 mini SliceBeam Export - Summary

## Export Results

Successfully exported **4 complete printer profiles** for the Bambu Lab A1 mini, each in both INI and ORCA_PRINTER formats for maximum SliceBeam compatibility.

### Generated Files

**Downloadable Archive**: `bambu_a1_mini_slicebeam_profiles.zip` (45KB)

**Individual Profiles**:
- **0.2mm nozzle**: `Bambu_Lab_A1_mini_02_nozzle.ini` + `.orca_printer`
- **0.4mm nozzle**: `Bambu_Lab_A1_mini_04_nozzle.ini` + `.orca_printer` 
- **0.6mm nozzle**: `Bambu_Lab_A1_mini_06_nozzle.ini` + `.orca_printer`
- **0.8mm nozzle**: `Bambu_Lab_A1_mini_08_nozzle.ini` + `.orca_printer`

### Profile Features

Each profile includes:
- ✅ Complete machine configuration (bed size: 180×180×180mm)
- ✅ Nozzle-specific settings for optimal print quality
- ✅ Temperature ranges for various filament types  
- ✅ A1 mini-specific start/end G-code
- ✅ Retraction settings optimized for direct drive extruder
- ✅ Speed and acceleration limits
- ✅ Bed leveling and calibration routines

### Usage Instructions

1. **Download**: Get the `bambu_a1_mini_slicebeam_profiles.zip` file
2. **Extract**: Unzip to access individual profile files
3. **Transfer**: Copy desired profiles to your Android device
4. **Import**: In SliceBeam app → Settings → Import Printer Profile
5. **Select**: Choose the profile matching your nozzle size

### Quality Verification

- ✅ All profiles exported successfully without errors
- ✅ Files contain correct printer model (Bambu Lab A1 mini)
- ✅ Nozzle diameters correctly set per variant
- ✅ Machine limits properly configured
- ✅ Archive integrity verified (no corruption)

### Technical Details

- **Export Method**: OrcaSlicer `export_for_slicebeam.py` tool
- **Inheritance**: Fully resolved from base profiles
- **Source**: Latest OrcaSlicer BBL vendor profiles
- **Formats**: Both INI (standard config) and ORCA_PRINTER (JSON metadata)
- **Compatibility**: SliceBeam Android app

---

**Ready for download and use with SliceBeam!**