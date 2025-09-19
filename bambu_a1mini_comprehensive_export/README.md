# Bambu Lab A1 mini Comprehensive SliceBeam Export

This directory contains **100 complete config bundles** for the **Bambu Lab A1 mini** 3D printer, each including printer, filament, and print profile combinations for maximum SliceBeam compatibility.

## What's Included

### Complete Setup Bundles
Each `.ini` file contains everything needed for SliceBeam:
- **[printer:...]** section with A1 mini hardware settings
- **[print:...]** section with specific layer height and quality settings  
- **[filament:...]** section with material-specific temperatures and settings
- **[presets]** section linking all components together

### Combination Coverage

**Printer Variants**: 2 most common nozzle sizes
- Bambu Lab A1 mini 0.2 nozzle (fine detail printing)
- Bambu Lab A1 mini 0.4 nozzle (standard printing)

**Filament Types**: 10 key materials including:
- **Bambu Brand**: PLA Basic, PLA Silk, PETG Basic, ABS, TPU 95A
- **Generic Materials**: PLA, PETG, ABS, TPU 
- **Various nozzle-specific variants** for optimal compatibility

**Print Quality Profiles**: 5 layer height options
- **0.08mm High Quality** - Ultra fine detail
- **0.12mm Fine** - High detail
- **0.16mm Optimal** - Balanced quality/speed  
- **0.20mm Standard** - Normal printing
- **0.24mm Draft** - Fast printing

### File Naming Convention

Files are named: `Printer--Filament--Process.ini`

Examples:
- `Bambu_Lab_A1_mini_04_nozzle--Bambu_PLA_Basic_BBL_A1M--020mm_Standard_BBL_A1M.ini`
- `Bambu_Lab_A1_mini_02_nozzle--Generic_PLA_BBL_A1M--008mm_High_Quality_BBL_A1M.ini`

## How to Use with SliceBeam

### Quick Setup
1. **Choose your bundle**: Select the `.ini` file that matches your:
   - Nozzle size (0.2mm or 0.4mm)
   - Filament type (PLA Basic, PETG, ABS, etc.)
   - Desired quality (0.08mm fine to 0.24mm draft)

2. **Transfer to Android**: Copy the selected `.ini` file to your Android device

3. **Import to SliceBeam**: 
   - Open SliceBeam app
   - Go to Settings → Import Printer Profile
   - Select your copied `.ini` file
   - Complete printer setup imports automatically!

### Popular Combinations

**For beginners (0.4mm nozzle + PLA + standard quality)**:
- `Bambu_Lab_A1_mini_04_nozzle--Bambu_PLA_Basic_BBL_A1M--020mm_Standard_BBL_A1M.ini`

**For fine detail work (0.2mm nozzle + PLA + high quality)**:
- `Bambu_Lab_A1_mini_02_nozzle--Bambu_PLA_Basic_BBL_A1M--008mm_High_Quality_BBL_A1M.ini`

**For fast prototyping (0.4mm nozzle + PLA + draft quality)**:
- `Bambu_Lab_A1_mini_04_nozzle--Generic_PLA_BBL_A1M--024mm_Draft_BBL_A1M.ini`

## Bundle Features

Each config bundle provides:

### Printer Configuration
- ✅ **Print bed**: 180×180×180mm volume
- ✅ **A1 mini G-code**: Proper start/end sequences with bed leveling
- ✅ **Hardware limits**: Speeds, accelerations, and temperature ranges
- ✅ **Nozzle-specific settings**: Optimized for 0.2mm or 0.4mm nozzles

### Print Profiles  
- ✅ **Layer heights**: From 0.08mm (ultra-fine) to 0.24mm (draft)
- ✅ **Speed settings**: Balanced for quality and print time
- ✅ **Support options**: Configurable automatic support generation
- ✅ **Infill patterns**: Grid pattern with appropriate density

### Filament Settings
- ✅ **Temperature profiles**: Optimized for each material type
- ✅ **Cooling settings**: Fan speeds and minimum layer times
- ✅ **Retraction tuning**: Direct drive extruder optimized
- ✅ **Flow rates**: Material-specific extrusion settings

## Compatibility

- **Generated from**: OrcaSlicer latest profiles (September 2024)
- **Compatible with**: SliceBeam Android app
- **Printer**: Bambu Lab A1 mini (all variants)
- **Format**: SliceBeam config bundle format (tested and verified)
- **Total combinations**: 100 complete setups

## Quality Assurance

- ✅ **Format verified**: All bundles use proper SliceBeam section structure
- ✅ **Inheritance resolved**: Settings properly merged from base profiles
- ✅ **A1 mini specific**: Hardware settings match printer capabilities
- ✅ **Material tested**: Filament profiles include proven temperature/cooling settings
- ✅ **Import tested**: Bundle format confirmed compatible with SliceBeam

## Support & Tips

### Choosing the Right Bundle
- **New users**: Start with 0.4mm nozzle + PLA Basic + 0.20mm Standard
- **Detail work**: Use 0.2mm nozzle + any PLA + 0.08mm High Quality  
- **Fast printing**: Use 0.4mm nozzle + any material + 0.24mm Draft
- **Engineering materials**: Choose ABS/PETG bundles for strength

### Troubleshooting
- **Import fails**: Ensure you're using a `.ini` file (not other formats)
- **Settings seem wrong**: Double-check you selected the bundle matching your nozzle
- **Print quality issues**: Try a different quality profile (layer height)

### Advanced Usage
- You can import multiple bundles to have different printer/material combinations available
- Switch between profiles in SliceBeam for different print jobs
- Each bundle is completely self-contained and independent

## Credits

Comprehensive profiles exported from OrcaSlicer using enhanced export tools with complete SliceBeam compatibility.

---

**Total: 100 ready-to-use SliceBeam config bundles for every A1 mini printing scenario!**