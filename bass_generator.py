"""
Bass Line Generator Module
Creates warm, fluid bass lines with algorithmic improvisation.
"""
import numpy as np
from typing import List, Tuple

class BassLineGenerator:
    """Generates harmonic bass lines with algorithmic variations."""
    
    # Chord progression for "A Dawn" (peaceful, ascending feel)
    CHORD_ROOTS = {
        'intro': [48, 48, 53, 53],      # C, C, F, F (low register)
        'development': [48, 53, 55, 52], # C, F, G, Em
        'climax': [48, 55, 53, 52],      # C, G, F, Em
        'ending': [48, 53, 48, 48],      # C, F, C, C
    }
    
    def __init__(self, seed: int = None):
        if seed:
            np.random.seed(seed)
        self.variation_probability = 0.3
    
    def generate_bass_pattern(self, root: int, beats: int = 4) -> List[Tuple[float, int, int, float]]:
        """
        Generate bass pattern for one chord.
        Returns: List of (beat_position, note, velocity, duration)
        """
        events = []
        current_beat = 0.0
        
        while current_beat < beats:
            # Decide note (root, fifth, or octave)
            if np.random.random() < self.variation_probability:
                interval = np.random.choice([0, 7, 12, -12])  # Root, 5th, octave up/down
            else:
                interval = 0
            
            note = root + interval
            velocity = np.random.randint(60, 85)
            
            # Rhythmic variation
            if np.random.random() < 0.7:
                duration = 1.0  # Quarter note
            else:
                duration = np.random.choice([0.5, 1.5, 2.0])
            
            events.append((current_beat, note, velocity, min(duration, beats - current_beat)))
            current_beat += duration
        
        return events
    
    def generate_section(self, section: str, bars: int = 4) -> List[Tuple[float, int, int, float]]:
        """Generate bass line for a section."""
        roots = self.CHORD_ROOTS.get(section, self.CHORD_ROOTS['intro'])
        events = []
        
        for bar in range(bars):
            root = roots[bar % len(roots)]
            pattern = self.generate_bass_pattern(root, 4)
            
            for beat, note, vel, dur in pattern:
                events.append((bar * 4 + beat, note, vel, dur))
        
        return events
    
    def generate_walking_bass(self, root: int, target: int, beats: int = 4) -> List[Tuple[float, int, int, float]]:
        """Generate walking bass line between two chord roots."""
        events = []
        steps = int(beats * 2)  # Eighth notes
        
        # Calculate chromatic/diatonic walk
        direction = 1 if target > root else -1
        current_note = root
        
        for i in range(steps):
            beat = i * 0.5
            velocity = 65 + np.random.randint(-10, 10)
            
            # Walk toward target with some randomness
            if np.random.random() < 0.7:
                step = direction * np.random.choice([1, 2])
            else:
                step = 0
            
            current_note = np.clip(current_note + step, min(root, target) - 5, max(root, target) + 5)
            events.append((beat, int(current_note), velocity, 0.5))
        
        return events
