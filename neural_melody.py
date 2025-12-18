"""
Neural Network Module for Melodic and Harmonic Suggestions
Uses a simple LSTM-based model for MIDI sequence generation.
"""
import numpy as np
from typing import List, Tuple, Optional

# Check if TensorFlow is available
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available. Using rule-based fallback.")

class MelodyDataset:
    """Generates training data for the neural network."""
    
    # Common chord progressions in C major (dawn-like, peaceful)
    CHORD_PROGRESSIONS = [
        [60, 64, 67],  # C major
        [65, 69, 72],  # F major
        [67, 71, 74],  # G major
        [57, 60, 64],  # Am
        [62, 65, 69],  # Dm
        [64, 67, 71],  # Em
    ]
    
    # Melodic patterns (relative intervals)
    MELODIC_PATTERNS = [
        [0, 2, 4, 5, 7, 5, 4, 2],
        [0, 4, 7, 12, 7, 4, 0, -5],
        [0, 2, 0, -2, 0, 4, 2, 0],
        [7, 5, 4, 2, 0, 2, 4, 5],
        [0, 0, 2, 2, 4, 4, 5, 7],
    ]
    
    @classmethod
    def generate_training_sequences(cls, num_sequences: int = 100, seq_length: int = 16) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data based on musical rules."""
        X, y = [], []
        
        for _ in range(num_sequences):
            # Pick random chord and pattern
            chord = cls.CHORD_PROGRESSIONS[np.random.randint(len(cls.CHORD_PROGRESSIONS))]
            pattern = cls.MELODIC_PATTERNS[np.random.randint(len(cls.MELODIC_PATTERNS))]
            root = chord[0]
            
            # Generate sequence
            sequence = []
            for i in range(seq_length):
                note = root + pattern[i % len(pattern)]
                velocity = np.random.randint(60, 100)
                duration = np.random.choice([0.25, 0.5, 1.0])
                sequence.append([note / 127.0, velocity / 127.0, duration])
            
            # Input is sequence[:-1], target is sequence[1:]
            X.append(sequence[:-1])
            y.append(sequence[-1])
        
        return np.array(X), np.array(y)

class NeuralMelodyGenerator:
    """LSTM-based neural network for melody generation."""
    
    def __init__(self, seq_length: int = 15):
        self.seq_length = seq_length
        self.model = None
        self.is_trained = False
    
    def build_model(self):
        """Build the LSTM model architecture."""
        if not TF_AVAILABLE:
            return
        
        self.model = Sequential([
            LSTM(64, input_shape=(self.seq_length, 3), return_sequences=True),
            Dropout(0.2),
            LSTM(32),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(3, activation='sigmoid')  # note, velocity, duration
        ])
        self.model.compile(optimizer='adam', loss='mse')
    
    def train(self, epochs: int = 50, verbose: int = 0):
        """Train the model on synthetic data."""
        if not TF_AVAILABLE:
            self.is_trained = True
            return
        
        X, y = MelodyDataset.generate_training_sequences(200, self.seq_length + 1)
        self.build_model()
        self.model.fit(X, y, epochs=epochs, batch_size=32, verbose=verbose)
        self.is_trained = True
    
    def generate_note(self, seed_sequence: np.ndarray) -> Tuple[int, int, float]:
        """Generate next note based on seed sequence."""
        if not TF_AVAILABLE or not self.is_trained:
            return self._fallback_generate()
        
        prediction = self.model.predict(seed_sequence.reshape(1, -1, 3), verbose=0)[0]
        note = int(prediction[0] * 127)
        velocity = int(prediction[1] * 127)
        duration = prediction[2] * 2  # Scale to 0-2 beats
        
        return note, velocity, max(0.25, duration)
    
    def _fallback_generate(self) -> Tuple[int, int, float]:
        """Rule-based fallback when TF not available."""
        # Generate notes in C major pentatonic (peaceful, dawn-like)
        scale = [60, 62, 64, 67, 69, 72, 74, 76, 79]
        note = np.random.choice(scale)
        velocity = np.random.randint(50, 90)
        duration = np.random.choice([0.5, 1.0, 1.5, 2.0])
        return note, velocity, duration
