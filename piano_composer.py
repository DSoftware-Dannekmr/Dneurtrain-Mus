"""
Piano Composition Module
Creates evocative, soft, melodic piano parts inspired by sunrise.
"""
import numpy as np
from typing import List, Tuple, Optional
from neural_melody import NeuralMelodyGenerator, TF_AVAILABLE

class PianoComposer:
    """Composes piano parts with neural network assistance."""
    
    # C major scale with extensions (peaceful, dawn-like)
    SCALE = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79]
    
    # Chord voicings (root position and inversions)
    CHORDS = {
        'C': [60, 64, 67, 72],
        'F': [65, 69, 72, 77],
        'G': [67, 71, 74, 79],
        'Am': [57, 60, 64, 69],
        'Em': [64, 67, 71, 76],
        'Dm': [62, 65, 69, 74],
    }
    
    # Progression for each section
    PROGRESSIONS = {
        'intro': ['C', 'Am', 'F', 'C'],
        'development': ['C', 'F', 'Am', 'G'],
        'climax': ['C', 'G', 'Am', 'F', 'C', 'G', 'F', 'C'],
        'ending': ['Am', 'F', 'C', 'C'],
    }
    
    def __init__(self, seed: int = None):
        if seed:
            np.random.seed(seed)
        self.neural_gen = NeuralMelodyGenerator()
        self.neural_gen.train(epochs=30, verbose=0)
    
    def generate_arpeggio(self, chord_name: str, beats: int = 4, 
                          velocity_range: Tuple[int, int] = (50, 70)) -> List[Tuple[float, int, int, float]]:
        """Generate arpeggiated chord pattern."""
        chord = self.CHORDS[chord_name]
        events = []
        
        patterns = [
            [0, 1, 2, 3, 2, 1],  # Up and down
            [0, 2, 1, 3, 2, 0],  # Broken
            [3, 2, 1, 0, 1, 2],  # Down and up
        ]
        pattern = patterns[np.random.randint(len(patterns))]
        
        step_duration = beats / len(pattern)
        for i, idx in enumerate(pattern):
            note = chord[idx % len(chord)]
            velocity = np.random.randint(*velocity_range)
            events.append((i * step_duration, note, velocity, step_duration * 1.5))
        
        return events
    
    def generate_melody(self, bars: int = 4, base_note: int = 72) -> List[Tuple[float, int, int, float]]:
        """Generate melodic line using neural network suggestions."""
        events = []
        current_beat = 0.0
        total_beats = bars * 4
        
        # Seed sequence for neural network
        seed = np.array([[n/127, 0.6, 0.5] for n in self.SCALE[:15]])
        
        while current_beat < total_beats:
            if TF_AVAILABLE and self.neural_gen.is_trained:
                note, velocity, duration = self.neural_gen.generate_note(seed)
                # Constrain to scale
                note = self._snap_to_scale(note)
            else:
                note = np.random.choice(self.SCALE)
                velocity = np.random.randint(55, 85)
                duration = np.random.choice([0.5, 1.0, 1.5])
            
            events.append((current_beat, note, velocity, duration))
            current_beat += duration
            
            # Update seed
            seed = np.roll(seed, -1, axis=0)
            seed[-1] = [note/127, velocity/127, duration/2]
        
        return events
    
    def _snap_to_scale(self, note: int) -> int:
        """Snap note to nearest scale degree."""
        octave = (note // 12) * 12
        pitch_class = note % 12
        scale_pcs = [n % 12 for n in self.SCALE]
        
        closest = min(scale_pcs, key=lambda x: abs(x - pitch_class))
        return octave + closest
    
    def generate_chord_hits(self, chord_name: str, beat: float, 
                           velocity: int = 60) -> List[Tuple[float, int, int, float]]:
        """Generate chord as simultaneous notes."""
        chord = self.CHORDS[chord_name]
        events = []
        for note in chord:
            vel_variation = velocity + np.random.randint(-5, 5)
            events.append((beat, note, vel_variation, 2.0))
        return events
