"""
Advanced Neural Network for MIDI Composition
Trains on external MIDI files and generates high-quality compositions
"""
import os
import numpy as np
from typing import List, Tuple, Optional, Dict, TYPE_CHECKING
from pathlib import Path
import pickle
import json

if TYPE_CHECKING:
    from tensorflow.keras.models import Model

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, Model
    from tensorflow.keras.layers import (
        LSTM, Dense, Dropout, Bidirectional, Attention,
        Input, Concatenate, Embedding, RepeatVector
    )
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    Model = None
    print("Warning: TensorFlow not available. Install with: pip install tensorflow")

try:
    import mido
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    print("Warning: mido not available. Install with: pip install mido")


class MIDIDataProcessor:
    """Process MIDI files into training data"""
    
    def __init__(self, max_sequence_length: int = 100):
        self.max_sequence_length = max_sequence_length
        self.note_range = (21, 108)  # Piano range
        self.velocity_range = (0, 127)
        self.duration_range = (0.25, 4.0)
    
    def extract_notes_from_midi(self, midi_file: str) -> List[Dict]:
        """Extract note events from MIDI file"""
        if not MIDO_AVAILABLE:
            return []
        
        try:
            mid = mido.MidiFile(midi_file)
            notes = []
            current_time = 0
            
            for track in mid.tracks:
                for msg in track:
                    current_time += msg.time
                    
                    if msg.type == 'note_on' and msg.velocity > 0:
                        notes.append({
                            'pitch': msg.note,
                            'velocity': msg.velocity,
                            'time': current_time,
                            'duration': 0.5  # Will be updated
                        })
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        # Find matching note_on
                        for note in reversed(notes):
                            if note['pitch'] == msg.note and note.get('duration', 0.5) == 0.5:
                                note['duration'] = current_time - note['time']
                                break
            
            return notes
        except Exception as e:
            print(f"Error processing {midi_file}: {e}")
            return []
    
    def normalize_note(self, note: Dict) -> np.ndarray:
        """Normalize note to feature vector"""
        pitch_norm = (note['pitch'] - self.note_range[0]) / (self.note_range[1] - self.note_range[0])
        velocity_norm = note['velocity'] / self.velocity_range[1]
        duration_norm = min(note['duration'], self.duration_range[1]) / self.duration_range[1]
        
        return np.array([pitch_norm, velocity_norm, duration_norm])
    
    def create_sequences(self, notes: List[Dict], seq_length: int = None) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for training"""
        if seq_length is None:
            seq_length = self.max_sequence_length
        
        if len(notes) < seq_length + 1:
            return np.array([]), np.array([])
        
        X, y = [], []
        
        for i in range(len(notes) - seq_length):
            sequence = np.array([self.normalize_note(notes[j]) for j in range(i, i + seq_length)])
            target = self.normalize_note(notes[i + seq_length])
            
            X.append(sequence)
            y.append(target)
        
        return np.array(X), np.array(y)
    
    def process_midi_directory(self, directory: str) -> Tuple[np.ndarray, np.ndarray]:
        """Process all MIDI files in directory"""
        X_all, y_all = [], []
        
        midi_files = list(Path(directory).glob('**/*.mid')) + list(Path(directory).glob('**/*.midi'))
        
        print(f"Found {len(midi_files)} MIDI files")
        
        for midi_file in midi_files:
            print(f"Processing {midi_file.name}...")
            notes = self.extract_notes_from_midi(str(midi_file))
            
            if notes:
                X, y = self.create_sequences(notes)
                if len(X) > 0:
                    X_all.append(X)
                    y_all.append(y)
        
        if X_all:
            X_combined = np.vstack(X_all)
            y_combined = np.vstack(y_all)
            return X_combined, y_combined
        
        return np.array([]), np.array([])


class AdvancedNeuralComposer:
    """Advanced neural network for music composition"""
    
    def __init__(self, seq_length: int = 100, model_name: str = "composer_model"):
        self.seq_length = seq_length
        self.model_name = model_name
        self.model = None
        self.is_trained = False
        self.training_history = None
        self.scaler_params = None
    
    def build_model(self, input_shape: Tuple[int, int]) -> 'Model':
        """Build advanced LSTM model with attention"""
        
        # Input layer
        inputs = Input(shape=input_shape)
        
        # Bidirectional LSTM layers
        x = Bidirectional(LSTM(256, return_sequences=True, dropout=0.2))(inputs)
        x = Bidirectional(LSTM(128, return_sequences=True, dropout=0.2))(x)
        
        # Attention mechanism
        attention = Attention()([x, x])
        x = Concatenate()([x, attention])
        
        # Dense layers
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.2)(x)
        
        # Output layer (3 features: pitch, velocity, duration)
        outputs = Dense(3, activation='sigmoid')(x[:, -1, :])
        
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        return model
    
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, 
              batch_size: int = 32, validation_split: float = 0.2):
        """Train the model"""
        
        if not TF_AVAILABLE:
            print("TensorFlow not available")
            return
        
        if len(X) == 0:
            print("No training data")
            return
        
        print(f"Training data shape: {X.shape}")
        print(f"Target data shape: {y.shape}")
        
        # Build model if not exists
        if self.model is None:
            self.build_model(X.shape[1:])
        
        # Callbacks
        early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.00001)
        
        # Train
        print("Starting training...")
        self.training_history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stop, reduce_lr],
            verbose=1
        )
        
        self.is_trained = True
        print("Training complete!")
    
    def generate_sequence(self, seed_sequence: np.ndarray, length: int = 100) -> np.ndarray:
        """Generate a sequence of notes"""
        
        if not self.is_trained or self.model is None:
            return np.array([])
        
        generated = list(seed_sequence)
        
        for _ in range(length):
            # Get last sequence
            current_seq = np.array(generated[-self.seq_length:]).reshape(1, self.seq_length, 3)
            
            # Predict next note
            next_note = self.model.predict(current_seq, verbose=0)[0]
            generated.append(next_note)
        
        return np.array(generated)
    
    def save_model(self, filepath: str = None):
        """Save trained model"""
        if filepath is None:
            filepath = f"{self.model_name}.h5"
        
        if self.model:
            self.model.save(filepath)
            print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str = None):
        """Load trained model"""
        if filepath is None:
            filepath = f"{self.model_name}.h5"
        
        if os.path.exists(filepath):
            self.model = tf.keras.models.load_model(filepath)
            self.is_trained = True
            print(f"Model loaded from {filepath}")
        else:
            print(f"Model file not found: {filepath}")


class EnhancedComposer:
    """Enhanced composer using neural network"""
    
    def __init__(self, neural_model: Optional[AdvancedNeuralComposer] = None):
        self.neural_model = neural_model
        self.note_range = (21, 108)
    
    def denormalize_note(self, normalized: np.ndarray) -> Dict:
        """Convert normalized values back to note"""
        pitch = int(normalized[0] * (self.note_range[1] - self.note_range[0]) + self.note_range[0])
        velocity = int(normalized[1] * 127)
        duration = normalized[2] * 4.0  # Max 4 beats
        
        return {
            'pitch': np.clip(pitch, self.note_range[0], self.note_range[1]),
            'velocity': np.clip(velocity, 0, 127),
            'duration': max(0.25, duration)
        }
    
    def generate_composition(self, seed_notes: List[Dict], length: int = 100) -> List[Dict]:
        """Generate composition using neural network"""
        
        if not self.neural_model or not self.neural_model.is_trained:
            return seed_notes
        
        # Normalize seed
        processor = MIDIDataProcessor()
        seed_normalized = np.array([processor.normalize_note(n) for n in seed_notes])
        
        # Generate
        generated_normalized = self.neural_model.generate_sequence(seed_normalized, length)
        
        # Denormalize
        composition = [self.denormalize_note(n) for n in generated_normalized]
        
        return composition
    
    def enhance_melody(self, melody: List[Dict]) -> List[Dict]:
        """Enhance melody using neural network"""
        
        if not self.neural_model or not self.neural_model.is_trained:
            return melody
        
        # Use neural network to suggest improvements
        enhanced = []
        
        for i, note in enumerate(melody):
            if i > 0:
                # Get context from previous notes
                context = melody[max(0, i-5):i]
                
                # Generate suggestion
                if len(context) >= 5:
                    processor = MIDIDataProcessor()
                    context_normalized = np.array([processor.normalize_note(n) for n in context])
                    
                    # Predict next
                    if self.neural_model.model:
                        prediction = self.neural_model.model.predict(
                            context_normalized.reshape(1, -1, 3), 
                            verbose=0
                        )[0]
                        
                        # Blend with original
                        blend_factor = 0.3
                        enhanced_note = {
                            'pitch': int(note['pitch'] * (1 - blend_factor) + 
                                       prediction[0] * 127 * blend_factor),
                            'velocity': int(note['velocity'] * (1 - blend_factor) + 
                                          prediction[1] * 127 * blend_factor),
                            'duration': note['duration'] * (1 - blend_factor) + 
                                       prediction[2] * 4.0 * blend_factor
                        }
                        enhanced.append(enhanced_note)
                    else:
                        enhanced.append(note)
                else:
                    enhanced.append(note)
            else:
                enhanced.append(note)
        
        return enhanced


def train_neural_composer(midi_directory: str, epochs: int = 100) -> AdvancedNeuralComposer:
    """Train neural composer on MIDI directory"""
    
    if not TF_AVAILABLE:
        print("TensorFlow not available")
        return None
    
    print(f"Training neural composer on {midi_directory}...")
    
    # Process MIDI files
    processor = MIDIDataProcessor()
    X, y = processor.process_midi_directory(midi_directory)
    
    if len(X) == 0:
        print("No training data found")
        return None
    
    # Create and train model
    composer = AdvancedNeuralComposer()
    composer.build_model(X.shape[1:])
    composer.train(X, y, epochs=epochs)
    
    # Save model
    composer.save_model()
    
    return composer


if __name__ == "__main__":
    # Example usage
    print("Advanced Neural Network Composer")
    print("=" * 50)
    
    # Check if MIDI directory exists
    midi_dir = "training_data"
    if os.path.exists(midi_dir):
        composer = train_neural_composer(midi_dir, epochs=50)
        if composer:
            print("✓ Neural composer trained successfully")
    else:
        print(f"Create a '{midi_dir}' folder with MIDI files to train")
