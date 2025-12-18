# Neural Network Training Guide

## Overview

The Universal Genre MIDI Composer now includes an advanced neural network system that can learn from your MIDI files and enhance compositions with learned patterns. This guide explains how to use the neural network features.

## Features

- **LSTM-based Architecture**: Bidirectional LSTM layers with attention mechanism
- **External MIDI Training**: Train on your own MIDI file collections
- **Model Persistence**: Save and load trained models
- **Seamless Integration**: Neural enhancements blend with algorithmic composition
- **Web Interface**: Easy-to-use training and generation controls

## Quick Start

### 1. Prepare Training Data

Create a `training_data` folder in the project directory and add MIDI files:

```
a_dawn_composer/
├── training_data/
│   ├── piano_piece_1.mid
│   ├── piano_piece_2.mid
│   ├── jazz_solo.mid
│   └── ... (more MIDI files)
```

**Recommended**: Use 50-100 MIDI files for good training results. The more diverse your training data, the better the model generalizes.

### 2. Train the Model

#### Via Web Interface:

1. Open the web application (http://localhost:8000)
2. Scroll to the "🧠 Red Neuronal" section
3. Set the training directory (default: `training_data`)
4. Set the number of epochs (50-100 recommended)
5. Enter a model name (default: `composer_model`)
6. Click "🎓 Entrenar Red Neuronal"

#### Via Command Line:

```python
from advanced_neural_network import train_neural_composer

# Train on MIDI directory
composer = train_neural_composer('training_data', epochs=100)

# Model is automatically saved to 'composer_model.h5'
```

### 3. Generate with Neural Enhancement

#### Via Web Interface:

1. Select a genre
2. Check the "Usar Red Neuronal" checkbox (only available if model is trained)
3. Click "▶ Generar MIDI"
4. Download the generated file (will have `_neural` suffix)

#### Via Python:

```python
from advanced_neural_network import AdvancedNeuralComposer
from universal_composer import GenreComposer

# Load trained model
neural_model = AdvancedNeuralComposer()
neural_model.load_model('models/composer_model.h5')

# Generate with neural enhancement
composer = GenreComposer('jazz_fusion', neural_model=neural_model)
melody = composer.generate_melody(bars=32)
```

## Technical Details

### Architecture

The neural network uses:

- **Input Layer**: Normalized MIDI note sequences (pitch, velocity, duration)
- **Bidirectional LSTM**: 256 units (first layer), 128 units (second layer)
- **Attention Mechanism**: Learns which parts of the sequence are most important
- **Dense Layers**: 256 → 128 units with dropout (0.2-0.3)
- **Output Layer**: 3 features (pitch, velocity, duration) with sigmoid activation

### Training Process

1. **Data Processing**:
   - Extracts note events from MIDI files
   - Normalizes values to 0-1 range
   - Creates sequences of 100 notes

2. **Model Training**:
   - Uses Adam optimizer with learning rate 0.001
   - Early stopping if validation loss doesn't improve
   - Learning rate reduction on plateau
   - Validation split: 20%

3. **Enhancement**:
   - Blends neural predictions with original compositions
   - Blend factor: 30% neural, 70% algorithmic
   - Maintains genre-specific characteristics

### Model Files

Models are saved in the `models/` directory:

```
models/
├── composer_model.h5          # Default model
├── jazz_specialist.h5         # Jazz-trained model
└── classical_composer.h5      # Classical-trained model
```

## Advanced Usage

### Train Multiple Specialized Models

```python
from advanced_neural_network import train_neural_composer

# Train jazz-specific model
jazz_composer = train_neural_composer('training_data/jazz', epochs=100)
jazz_composer.save_model('models/jazz_specialist.h5')

# Train classical-specific model
classical_composer = train_neural_composer('training_data/classical', epochs=100)
classical_composer.save_model('models/classical_composer.h5')
```

### Adjust Neural Influence

Edit the blend factor in `advanced_neural_network.py`:

```python
# In EnhancedComposer.enhance_melody()
blend_factor = 0.5  # Increase for more neural influence (0.0-1.0)
```

### Monitor Training

The training process shows:
- Number of MIDI files found
- Training data shape
- Epoch progress with loss metrics
- Validation loss tracking

## Troubleshooting

### "TensorFlow not available"

Install TensorFlow:
```bash
pip install tensorflow
```

### "No training data found"

- Check that MIDI files are in the specified directory
- Ensure files have `.mid` or `.midi` extension
- Verify files are valid MIDI format

### Model not loading

- Check that model file exists in `models/` directory
- Verify file path is correct
- Ensure TensorFlow version matches training version

### Poor generation quality

- Use more training data (100+ files)
- Increase epochs (100-200)
- Use diverse MIDI files
- Adjust blend factor for more neural influence

## Performance Tips

1. **Training Speed**:
   - GPU acceleration: Install `tensorflow-gpu`
   - Batch size: Adjust in `train()` method
   - Epochs: Start with 50, increase if needed

2. **Generation Quality**:
   - More training data = better results
   - Longer training = better convergence
   - Diverse genres = more versatile model

3. **Memory Usage**:
   - Reduce sequence length if out of memory
   - Use smaller batch sizes
   - Process MIDI files in batches

## API Reference

### AdvancedNeuralComposer

```python
# Initialize
composer = AdvancedNeuralComposer(seq_length=100, model_name="composer_model")

# Build model
composer.build_model(input_shape=(100, 3))

# Train
composer.train(X, y, epochs=100, batch_size=32, validation_split=0.2)

# Generate
sequence = composer.generate_sequence(seed_sequence, length=100)

# Save/Load
composer.save_model('path/to/model.h5')
composer.load_model('path/to/model.h5')
```

### EnhancedComposer

```python
# Initialize with neural model
enhanced = EnhancedComposer(neural_model=composer)

# Generate composition
composition = enhanced.generate_composition(seed_notes, length=100)

# Enhance melody
enhanced_melody = enhanced.enhance_melody(melody)
```

### MIDIDataProcessor

```python
# Initialize
processor = MIDIDataProcessor(max_sequence_length=100)

# Extract notes from MIDI
notes = processor.extract_notes_from_midi('file.mid')

# Create training sequences
X, y = processor.create_sequences(notes)

# Process entire directory
X_all, y_all = processor.process_midi_directory('training_data')
```

## Examples

### Example 1: Train and Generate

```python
from advanced_neural_network import train_neural_composer
from universal_composer import GenreComposer
from midiutil import MIDIFile

# Train model
print("Training neural model...")
neural_model = train_neural_composer('training_data', epochs=50)

# Generate composition
print("Generating composition...")
composer = GenreComposer('jazz_fusion', neural_model=neural_model)
melody = composer.generate_melody(bars=32)
bass = composer.generate_bass_line(bars=32)
chords = composer.generate_chords(bars=32)
drums = composer.generate_drum_pattern(bars=32)

# Save to MIDI
midi = MIDIFile(4)
# ... add tracks ...
with open('output.mid', 'wb') as f:
    midi.writeFile(f)
```

### Example 2: Compare Algorithmic vs Neural

```python
from universal_composer import GenreComposer

# Algorithmic only
composer_algo = GenreComposer('trap')
melody_algo = composer_algo.generate_melody(bars=16)

# With neural enhancement
neural_model = AdvancedNeuralComposer()
neural_model.load_model('models/composer_model.h5')
composer_neural = GenreComposer('trap', neural_model=neural_model)
melody_neural = composer_neural.generate_melody(bars=16)

# Compare results
print(f"Algorithmic: {len(melody_algo)} notes")
print(f"Neural: {len(melody_neural)} notes")
```

## Future Enhancements

- [ ] Real-time training progress in web UI
- [ ] Multiple model management
- [ ] Genre-specific model training
- [ ] Model comparison tools
- [ ] MIDI file upload for training
- [ ] Batch generation with neural models
- [ ] Model fine-tuning capabilities

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API reference
3. Check TensorFlow documentation
4. Verify MIDI file format

---

**Version**: 1.0  
**Last Updated**: December 2025  
**Requires**: TensorFlow 2.x, mido, midiutil
