# Installation & Dependency Fix Guide

## Issue: Missing Dependencies

If you see warnings like:
```
Warning: TensorFlow not available. Install with: pip install tensorflow
Warning: mido not available. Install with: pip install mido
```

This is normal and expected. The neural network features are optional.

## Solution: Install Dependencies

### Step 1: Install Required Dependencies

```bash
pip install midiutil numpy mido
```

### Step 2: Install Optional Neural Network Dependencies

For neural network features, install TensorFlow:

```bash
pip install tensorflow
```

**Note**: TensorFlow is large (~500MB) and optional. The system works without it, but neural features won't be available.

### Step 3: Verify Installation

```bash
python -c "import midiutil; import numpy; import mido; print('✓ Core dependencies installed')"
```

For neural features:
```bash
python -c "import tensorflow; print('✓ TensorFlow installed')"
```

## Complete Installation Steps

### Windows

1. **Open Command Prompt** (cmd.exe)

2. **Navigate to project directory**:
   ```bash
   cd "path\to\Compositor Neural Global - GEMINI KIRO\a_dawn_composer"
   ```

3. **Install dependencies**:
   ```bash
   pip install midiutil numpy mido
   ```

4. **Install TensorFlow (optional)**:
   ```bash
   pip install tensorflow
   ```

5. **Verify**:
   ```bash
   python -c "import midiutil; print('✓ Ready to use')"
   ```

### macOS/Linux

1. **Open Terminal**

2. **Navigate to project directory**:
   ```bash
   cd path/to/a_dawn_composer
   ```

3. **Install dependencies**:
   ```bash
   pip install midiutil numpy mido
   ```

4. **Install TensorFlow (optional)**:
   ```bash
   pip install tensorflow
   ```

5. **Verify**:
   ```bash
   python -c "import midiutil; print('✓ Ready to use')"
   ```

## Troubleshooting

### "Python not found"

**Windows**:
1. Install Python from https://www.python.org/downloads/
2. During installation, **check "Add Python to PATH"**
3. Restart Command Prompt
4. Try again

**macOS**:
```bash
brew install python3
```

**Linux**:
```bash
sudo apt-get install python3 python3-pip
```

### "pip not found"

Try using `pip3` instead:
```bash
pip3 install midiutil numpy mido
```

### "Permission denied"

Add `--user` flag:
```bash
pip install --user midiutil numpy mido
```

### "TensorFlow installation fails"

TensorFlow can be large. Try:
```bash
pip install --upgrade pip
pip install tensorflow
```

If still failing, you can use the system without neural features.

## What Works Without TensorFlow

✓ Generate music in 200+ genres
✓ Use web interface
✓ Use command-line generation
✓ Use Python API
✓ All algorithmic features

## What Requires TensorFlow

✓ Train neural models
✓ Use neural enhancement in generation
✓ Advanced neural features

## Minimal Installation

If you only want basic generation (no neural):

```bash
pip install midiutil numpy
```

## Full Installation

For all features including neural:

```bash
pip install midiutil numpy mido tensorflow
```

## Using the System

### Without Neural Features

```bash
# Generate music
python generate_any_genre.py trap -b 32

# Start web server
python web_server.py
```

### With Neural Features

```bash
# Train a model
python train_neural.py -e 100

# Generate with neural enhancement
# Use web interface or Python API
```

## Requirements File

All dependencies are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Virtual Environment (Recommended)

For a clean installation, use a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Docker (Advanced)

If you prefer Docker:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "web_server.py"]
```

## Getting Help

If you encounter issues:

1. Check this file for your specific error
2. Read `NEURAL_QUICK_START.md`
3. Check `NEURAL_NETWORK_GUIDE.md` troubleshooting section
4. Verify Python version: `python --version` (should be 3.7+)
5. Verify pip: `pip --version`

## Next Steps

After installing dependencies:

1. Read `NEURAL_QUICK_START.md`
2. Create `training_data/` folder
3. Add MIDI files
4. Run `python train_neural.py` or start web server
5. Generate enhanced music!

---

**Version**: 1.0  
**Last Updated**: December 2025
