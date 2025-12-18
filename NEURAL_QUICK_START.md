# Neural Network Quick Start

Get started with neural network training in 5 minutes!

## Step 1: Prepare Training Data (2 min)

1. Create a folder called `training_data` in the project directory
2. Add 20-50 MIDI files to this folder
   - Can be any genre or style
   - Mix different genres for versatility
   - Files should be `.mid` or `.midi` format

```
a_dawn_composer/
├── training_data/
│   ├── song1.mid
│   ├── song2.mid
│   ├── song3.mid
│   └── ... (more MIDI files)
```

## Step 2: Train the Model (1-5 min)

### Option A: Web Interface (Easiest)

1. Start the web server:
   ```bash
   python web_server.py
   ```

2. Open http://localhost:8000 in your browser

3. Scroll down to "🧠 Red Neuronal" section

4. Click "🎓 Entrenar Red Neuronal"

5. Wait for training to complete (progress bar shows status)

### Option B: Command Line

```bash
python train_neural.py
```

Or with custom settings:
```bash
python train_neural.py -d training_data -e 100 -m my_model
```

## Step 3: Generate with Neural Enhancement (1 min)

### Via Web Interface

1. Select a genre (e.g., "jazz_fusion")
2. Check the box "Usar Red Neuronal"
3. Click "▶ Generar MIDI"
4. Download the generated file

### Via Python

```python
from advanced_neural_network import AdvancedNeuralComposer
from universal_composer import GenreComposer

# Load model
neural_model = AdvancedNeuralComposer()
neural_model.load_model('models/composer_model.h5')

# Generate
composer = GenreComposer('trap', neural_model=neural_model)
melody = composer.generate_melody(bars=32)
```

## Troubleshooting

### "No training data found"
- Check that `training_data/` folder exists
- Verify MIDI files are in the folder
- Ensure files have `.mid` or `.midi` extension

### "TensorFlow not available"
```bash
pip install tensorflow
```

### "Model not loading"
- Check that `models/` folder exists
- Verify model file is named `composer_model.h5`
- Ensure TensorFlow is installed

## Tips for Best Results

1. **More Data = Better Results**
   - Use 50-100 MIDI files for good quality
   - Mix different genres for versatility

2. **Train Longer**
   - Start with 50 epochs
   - Increase to 100-200 for better results
   - More epochs = longer training time

3. **Diverse Training Data**
   - Mix different genres
   - Include different instruments
   - Vary tempo and complexity

4. **Use Appropriate Genres**
   - Train on jazz files → use with jazz genres
   - Train on electronic files → use with electronic genres
   - Train on mixed files → works with any genre

## Next Steps

- Read `NEURAL_NETWORK_GUIDE.md` for advanced features
- Experiment with different training data
- Train multiple models for different styles
- Combine neural enhancement with different genres

## Common Commands

```bash
# Train with defaults
python train_neural.py

# Train with 200 epochs
python train_neural.py -e 200

# Train on custom directory
python train_neural.py -d my_midi_files

# Train and save as custom model
python train_neural.py -m jazz_model

# List available models
python train_neural.py --list-models

# Start web server
python web_server.py

# Generate specific genre
python generate_any_genre.py trap -b 32
```

## File Locations

- **Training data**: `training_data/` (create this folder)
- **Trained models**: `models/` (auto-created)
- **Generated MIDI**: `output/` (auto-created)
- **Training script**: `train_neural.py`
- **Web server**: `web_server.py`

## Performance

- **Training time**: 50 epochs on 100 files ≈ 5-15 minutes (CPU)
- **Generation time**: ~100-200ms per composition
- **Model size**: ~5-10 MB per trained model

## Support

For more information:
- See `NEURAL_NETWORK_GUIDE.md` for detailed documentation
- Check `NEURAL_INTEGRATION_SUMMARY.md` for technical details
- Review error messages for specific issues

---

**Ready to create AI-enhanced music? Start training now!** 🎵🧠
