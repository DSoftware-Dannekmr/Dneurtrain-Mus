# Comprehensive Troubleshooting Guide

## Common Issues and Solutions

---

## 🔴 Training Issues

### Issue: "No MIDI files found in training_data"

**Error Message**:
```
No MIDI files found in training_data. Add .mid or .midi files to the directory.
```

**Causes**:
- `training_data` folder doesn't exist
- Folder is empty
- Files don't have `.mid` or `.midi` extension
- Files are in wrong location

**Solutions**:

1. **Create the folder**:
   ```bash
   mkdir training_data
   ```

2. **Add MIDI files**:
   - Download MIDI files from https://www.freemidi.org/
   - Copy them to `training_data/` folder
   - Verify files end with `.mid` or `.midi`

3. **Verify setup**:
   ```bash
   ls training_data/
   ```
   Should show MIDI files

4. **Check file extensions**:
   - Windows: Right-click file → Properties → check extension
   - macOS/Linux: `file training_data/*`

**See Also**: `TRAINING_DATA_SETUP.md`

---

### Issue: "Directory not found: training_data"

**Error Message**:
```
Directory not found: training_data. Create the directory and add MIDI files.
```

**Solution**:
```bash
# Create the directory
mkdir training_data

# Add MIDI files to it
# Then try training again
```

---

### Issue: Training starts but fails

**Possible Causes**:
- MIDI files are corrupted
- Not enough disk space
- TensorFlow not installed
- Out of memory

**Solutions**:

1. **Check TensorFlow**:
   ```bash
   python -c "import tensorflow; print('✓ TensorFlow installed')"
   ```
   If error, install: `pip install tensorflow`

2. **Try with fewer files**:
   - Start with 5-10 MIDI files
   - Gradually add more

3. **Check disk space**:
   - Need ~1-2 GB free space
   - Models are ~5-10 MB each

4. **Try different MIDI files**:
   - Some files might be corrupted
   - Download from different source

5. **Reduce epochs**:
   ```bash
   python train_neural.py -e 10
   ```

---

### Issue: Training is very slow

**Possible Causes**:
- Using CPU instead of GPU
- Too many MIDI files
- Too many epochs

**Solutions**:

1. **Use GPU** (if available):
   - Install CUDA and cuDNN
   - TensorFlow will auto-detect GPU

2. **Reduce training data**:
   - Start with 20-30 files
   - Increase gradually

3. **Reduce epochs**:
   ```bash
   python train_neural.py -e 25
   ```

4. **Check system resources**:
   - Close other applications
   - Free up RAM

---

## 🔴 Generation Issues

### Issue: "Model not loading"

**Error Message**:
```
Model not loading
```

**Causes**:
- Model file doesn't exist
- Model file is corrupted
- TensorFlow version mismatch

**Solutions**:

1. **Check model exists**:
   ```bash
   ls models/
   ```
   Should show `composer_model.h5`

2. **Verify model file**:
   ```bash
   file models/composer_model.h5
   ```
   Should show it's a valid file

3. **Reinstall TensorFlow**:
   ```bash
   pip install --upgrade tensorflow
   ```

4. **Train a new model**:
   ```bash
   python train_neural.py
   ```

---

### Issue: Neural checkbox is disabled

**Causes**:
- Model not trained yet
- Model file missing
- TensorFlow not installed

**Solutions**:

1. **Train a model**:
   ```bash
   python train_neural.py
   ```

2. **Check model exists**:
   ```bash
   ls models/composer_model.h5
   ```

3. **Install TensorFlow**:
   ```bash
   pip install tensorflow
   ```

4. **Restart web server**:
   - Stop: Ctrl+C
   - Start: `python web_server.py`

---

### Issue: Generation is slow

**Causes**:
- Using CPU
- Large model
- System resources low

**Solutions**:

1. **Use GPU** (if available)
2. **Close other applications**
3. **Reduce number of bars**
4. **Use smaller model**

---

## 🔴 Web Interface Issues

### Issue: "Failed to load resource: 400"

**Error Message**:
```
Failed to load resource: the server responded with a status of 400
```

**Causes**:
- Missing training data
- Invalid parameters
- Server error

**Solutions**:

1. **Check training data**:
   - Create `training_data/` folder
   - Add MIDI files
   - See `TRAINING_DATA_SETUP.md`

2. **Check parameters**:
   - Epochs should be 10-500
   - Directory should exist
   - Model name should be valid

3. **Check server logs**:
   - Look at terminal where server is running
   - Check for error messages

---

### Issue: "SyntaxError: Unexpected token '<'"

**Error Message**:
```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

**Causes**:
- Server returned HTML error page instead of JSON
- Server crashed or returned error

**Solutions**:

1. **Check server logs**:
   - Look at terminal where server is running
   - Check for error messages

2. **Restart server**:
   ```bash
   # Stop: Ctrl+C
   # Start: python web_server.py
   ```

3. **Check training data**:
   - Verify `training_data/` folder exists
   - Verify MIDI files are present

4. **Check dependencies**:
   ```bash
   python check_installation.py
   ```

---

### Issue: Web interface won't load

**Error Message**:
```
Cannot GET /
```

**Causes**:
- Server not running
- Wrong port
- Firewall blocking

**Solutions**:

1. **Start server**:
   ```bash
   python web_server.py
   ```

2. **Check port**:
   - Default: http://localhost:8000
   - Check terminal for actual port

3. **Check firewall**:
   - Allow Python through firewall
   - Try different port

4. **Check browser**:
   - Try different browser
   - Clear cache: Ctrl+Shift+Delete

---

## 🔴 Installation Issues

### Issue: "TensorFlow not available"

**Warning Message**:
```
Warning: TensorFlow not available. Install with: pip install tensorflow
```

**This is normal!** TensorFlow is optional.

**To enable neural features**:
```bash
pip install tensorflow
```

**To use without neural features**:
- Just ignore the warning
- System works fine without it

---

### Issue: "mido not available"

**Warning Message**:
```
Warning: mido not available. Install with: pip install mido
```

**This is normal!** mido is optional for training.

**To enable training**:
```bash
pip install mido
```

**To use without training**:
- Just ignore the warning
- Can still generate music

---

### Issue: "pip: command not found"

**Causes**:
- Python not installed
- Python not in PATH
- Using wrong command

**Solutions**:

**Windows**:
1. Install Python from https://www.python.org/downloads/
2. **Check "Add Python to PATH"** during installation
3. Restart Command Prompt
4. Try again

**macOS**:
```bash
# Use pip3 instead
pip3 install tensorflow

# Or install Python
brew install python3
```

**Linux**:
```bash
# Use pip3 instead
pip3 install tensorflow

# Or install Python
sudo apt-get install python3-pip
```

---

### Issue: "Permission denied"

**Error Message**:
```
Permission denied
```

**Solution**:
```bash
pip install --user tensorflow
```

Or use virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install tensorflow
```

---

## 🔴 Python Issues

### Issue: "Python not found"

**Error Message**:
```
'python' is not recognized as an internal or external command
```

**Solutions**:

**Windows**:
1. Install Python from https://www.python.org/downloads/
2. **Check "Add Python to PATH"** during installation
3. Restart Command Prompt
4. Try: `python --version`

**macOS**:
```bash
# Check if Python is installed
python3 --version

# If not, install it
brew install python3
```

**Linux**:
```bash
# Check if Python is installed
python3 --version

# If not, install it
sudo apt-get install python3
```

---

### Issue: "ModuleNotFoundError: No module named 'X'"

**Error Message**:
```
ModuleNotFoundError: No module named 'midiutil'
```

**Solution**:
```bash
pip install midiutil
```

**For all dependencies**:
```bash
pip install midiutil numpy mido tensorflow
```

---

## 🟡 Performance Issues

### Issue: Generation is slow

**Causes**:
- Using CPU instead of GPU
- System resources low
- Large model

**Solutions**:

1. **Use GPU** (if available):
   - Install CUDA and cuDNN
   - TensorFlow will auto-detect

2. **Close other applications**:
   - Free up RAM
   - Reduce CPU load

3. **Reduce generation size**:
   - Use fewer bars
   - Use smaller model

---

### Issue: Training is very slow

**Causes**:
- Using CPU
- Too many files
- Too many epochs

**Solutions**:

1. **Use GPU** (if available)
2. **Reduce training data** (start with 20 files)
3. **Reduce epochs** (start with 25)
4. **Close other applications**

---

## 🟡 Quality Issues

### Issue: Generated music quality is poor

**Causes**:
- Not enough training data
- Not enough epochs
- Poor quality training data

**Solutions**:

1. **Use more training data**:
   - Start with 50-100 files
   - Mix different genres

2. **Train longer**:
   - Increase epochs to 100-200
   - Takes longer but better results

3. **Use better training data**:
   - Use high-quality MIDI files
   - Avoid corrupted files
   - Use diverse genres

4. **Adjust blend factor**:
   - Edit `advanced_neural_network.py`
   - Increase `blend_factor` for more neural influence

---

## 🟢 Verification Checklist

### Before Training
- [ ] `training_data/` folder exists
- [ ] MIDI files are in folder
- [ ] Files have `.mid` or `.midi` extension
- [ ] At least 5 MIDI files present
- [ ] TensorFlow installed (optional)
- [ ] mido installed (optional)

### Before Generating
- [ ] Model file exists in `models/`
- [ ] Web server is running
- [ ] Browser can access http://localhost:8000
- [ ] Neural checkbox is enabled

### System Check
- [ ] Python 3.7+ installed
- [ ] pip working
- [ ] Enough disk space (1-2 GB)
- [ ] Enough RAM (2-4 GB)

---

## 📞 Getting Help

### Documentation
- `NEURAL_QUICK_START.md` - Quick start
- `NEURAL_NETWORK_GUIDE.md` - Comprehensive guide
- `TRAINING_DATA_SETUP.md` - Training data setup
- `INSTALLATION_FIX.md` - Installation help
- `DEPENDENCY_RESOLUTION.md` - Dependency help

### Tools
- `check_installation.py` - Verify installation
- `train_neural.py` - Training script
- `web_server.py` - Web interface

### Steps to Get Help
1. Check this guide
2. Check relevant documentation
3. Run `python check_installation.py`
4. Check server logs (terminal)
5. Verify folder structure
6. Try with minimal setup (5 MIDI files)

---

## 🔧 Debug Mode

### Enable Verbose Output

**Training**:
```bash
python train_neural.py -e 10
# Watch terminal for detailed output
```

**Web Server**:
```bash
python web_server.py
# Watch terminal for request logs
```

### Check Installation

```bash
python check_installation.py
```

Shows:
- ✓ for installed dependencies
- ✗ for missing dependencies
- Module import status

### Manual Verification

```bash
# Check each dependency
python -c "import midiutil; print('✓ midiutil')"
python -c "import numpy; print('✓ numpy')"
python -c "import mido; print('✓ mido')"
python -c "import tensorflow; print('✓ tensorflow')"

# Check genres
python -c "from genres.all_genres import get_genre_count; print(f'Genres: {get_genre_count()}')"

# Check composer
python -c "from universal_composer import GenreComposer; print('✓ GenreComposer')"

# Check neural
python -c "from advanced_neural_network import AdvancedNeuralComposer; print('✓ Neural')"
```

---

## 📋 Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "No MIDI files found" | Empty training_data folder | Add MIDI files |
| "Directory not found" | training_data doesn't exist | Create folder |
| "TensorFlow not available" | TensorFlow not installed | `pip install tensorflow` |
| "mido not available" | mido not installed | `pip install mido` |
| "Model not loading" | Model file missing | Train a model |
| "Permission denied" | Insufficient permissions | Use `--user` flag |
| "Python not found" | Python not in PATH | Reinstall Python |
| "Module not found" | Dependency not installed | `pip install <module>` |

---

## 🎯 Quick Fixes

### "It's not working!"

Try these in order:

1. **Restart everything**:
   ```bash
   # Stop server (Ctrl+C)
   # Restart: python web_server.py
   ```

2. **Check installation**:
   ```bash
   python check_installation.py
   ```

3. **Verify training data**:
   ```bash
   ls training_data/
   ```

4. **Try minimal setup**:
   - Use 5 MIDI files
   - Use 10 epochs
   - Try again

5. **Check documentation**:
   - Read `NEURAL_QUICK_START.md`
   - Read `TRAINING_DATA_SETUP.md`

6. **Check logs**:
   - Look at terminal output
   - Check for error messages

---

**Version**: 1.0  
**Last Updated**: December 2025

**Still having issues?** Check the documentation or try the quick fixes above! 🎵🧠
