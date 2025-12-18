# Training Data Setup Guide

## Problem: "No MIDI files found"

If you see this error when trying to train:
```
No MIDI files found in training_data. Add .mid or .midi files to the directory.
```

This guide will help you set up your training data correctly.

---

## Step 1: Create the Training Data Folder

### Windows
1. Open File Explorer
2. Navigate to: `C:\Users\Danny\Desktop\Compositor Neural Global - GEMINI KIRO\a_dawn_composer`
3. Right-click in empty space
4. Select "New" → "Folder"
5. Name it: `training_data`

### macOS/Linux
```bash
cd path/to/a_dawn_composer
mkdir training_data
```

---

## Step 2: Add MIDI Files

### Where to Get MIDI Files

1. **Free MIDI Collections**:
   - https://www.freemidi.org/
   - https://www.midiworld.com/
   - https://www.mutopiaproject.org/
   - https://www.classicforkids.com/

2. **Your Own MIDI Files**:
   - Export from your DAW (Ableton, FL Studio, Logic, etc.)
   - Download from music websites
   - Use existing MIDI files you have

3. **Recommended**:
   - Start with 20-50 MIDI files
   - Mix different genres for versatility
   - Use files that are 1-5 minutes long

### How to Add Files

1. Download MIDI files (`.mid` or `.midi` extension)
2. Copy them to the `training_data` folder
3. Verify they're there:
   - Windows: Open File Explorer, navigate to `training_data`
   - macOS/Linux: `ls training_data/`

---

## Step 3: Verify Setup

### Check Folder Structure

Your folder should look like this:

```
a_dawn_composer/
├── training_data/
│   ├── song1.mid
│   ├── song2.mid
│   ├── song3.mid
│   ├── jazz_piece.mid
│   ├── classical_music.mid
│   └── ... (more MIDI files)
├── web_server.py
├── train_neural.py
└── ... (other files)
```

### Verify Files

**Windows**:
1. Open File Explorer
2. Navigate to `training_data` folder
3. You should see `.mid` or `.midi` files

**macOS/Linux**:
```bash
ls -la training_data/
```

You should see output like:
```
total 1024
-rw-r--r--  1 user  staff  12345 Dec 18 10:00 song1.mid
-rw-r--r--  1 user  staff  23456 Dec 18 10:01 song2.mid
-rw-r--r--  1 user  staff  34567 Dec 18 10:02 song3.mid
```

---

## Step 4: Train the Model

### Via Web Interface

1. Open http://localhost:8000
2. Scroll to "🧠 Red Neuronal"
3. Verify "training_data" is in the directory field
4. Click "🎓 Entrenar Red Neuronal"
5. Wait for training to complete

### Via Command Line

```bash
python train_neural.py
```

Or with custom settings:
```bash
python train_neural.py -d training_data -e 100
```

---

## Troubleshooting

### "Directory not found: training_data"

**Solution**: Create the `training_data` folder in the `a_dawn_composer` directory

```bash
mkdir training_data
```

### "No MIDI files found in training_data"

**Solution**: Add MIDI files to the folder

1. Download MIDI files
2. Copy them to `training_data/`
3. Verify they have `.mid` or `.midi` extension
4. Try training again

### "Files are there but still getting error"

**Check file extensions**:
- Files must end with `.mid` or `.midi`
- Not `.txt`, `.mp3`, `.wav`, etc.

**Verify files are valid MIDI**:
```bash
# Try opening a file with a text editor
# It should start with "MThd" (MIDI header)
```

### "Training starts but fails"

**Possible causes**:
- MIDI files are corrupted
- MIDI files are too small
- Not enough disk space
- TensorFlow not installed

**Solution**:
1. Try with different MIDI files
2. Ensure TensorFlow is installed: `pip install tensorflow`
3. Check disk space

---

## Tips for Best Results

### File Selection

✓ **Good**: Mix different genres and styles
✓ **Good**: Use 50-100 files for best results
✓ **Good**: Use files 1-5 minutes long
✓ **Good**: Use high-quality MIDI files

✗ **Avoid**: All files from same genre
✗ **Avoid**: Very short files (<30 seconds)
✗ **Avoid**: Very long files (>10 minutes)
✗ **Avoid**: Corrupted or invalid MIDI files

### Training Parameters

- **Epochs**: Start with 50, increase to 100-200 for better results
- **Batch Size**: Default 32 is good for most cases
- **Validation Split**: Default 20% is good

### Training Time

- 50 epochs on 100 files: ~5-15 minutes (CPU)
- 100 epochs on 100 files: ~10-30 minutes (CPU)
- GPU: 2-5x faster

---

## Example Setup

### Quick Start (5 files)

```
training_data/
├── piano_piece_1.mid
├── piano_piece_2.mid
├── jazz_solo.mid
├── classical_music.mid
└── modern_composition.mid
```

### Standard Setup (50 files)

```
training_data/
├── jazz/
│   ├── jazz_1.mid
│   ├── jazz_2.mid
│   └── ... (10 files)
├── classical/
│   ├── classical_1.mid
│   ├── classical_2.mid
│   └── ... (10 files)
├── electronic/
│   ├── electronic_1.mid
│   ├── electronic_2.mid
│   └── ... (10 files)
├── pop/
│   ├── pop_1.mid
│   ├── pop_2.mid
│   └── ... (10 files)
└── world/
    ├── world_1.mid
    ├── world_2.mid
    └── ... (10 files)
```

### Advanced Setup (100+ files)

Organize by genre or style for specialized models:

```
training_data/
├── jazz_files/
│   └── (50 jazz MIDI files)
├── classical_files/
│   └── (50 classical MIDI files)
└── electronic_files/
    └── (50 electronic MIDI files)
```

Then train separate models:
```bash
python train_neural.py -d training_data/jazz_files -m jazz_model
python train_neural.py -d training_data/classical_files -m classical_model
python train_neural.py -d training_data/electronic_files -m electronic_model
```

---

## Verification Checklist

- [ ] `training_data` folder exists
- [ ] MIDI files are in `training_data` folder
- [ ] Files have `.mid` or `.midi` extension
- [ ] At least 5 MIDI files present
- [ ] Files are valid MIDI format
- [ ] Folder path is correct
- [ ] TensorFlow is installed (optional)
- [ ] Enough disk space available

---

## Next Steps

1. **Create `training_data` folder**
2. **Add MIDI files**
3. **Verify setup** (check folder structure)
4. **Train model**:
   - Via web: http://localhost:8000 → Neural section
   - Via CLI: `python train_neural.py`
5. **Generate enhanced music**

---

## Support

### Documentation
- `NEURAL_QUICK_START.md` - Quick start guide
- `NEURAL_NETWORK_GUIDE.md` - Comprehensive guide
- `INSTALLATION_FIX.md` - Installation help

### Tools
- `check_installation.py` - Verify installation
- `train_neural.py` - Training script
- `web_server.py` - Web interface

### Getting Help
1. Check this guide
2. Verify folder structure
3. Verify MIDI files are present
4. Check file extensions
5. Read the documentation

---

**Version**: 1.0  
**Last Updated**: December 2025

**Ready to train your neural model?** 🎵🧠
