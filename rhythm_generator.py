"""
Algorithmic Rhythm Generation Module
Uses Markov chains, random walk, and fractal variations for drum patterns.
"""
import numpy as np
from typing import List, Tuple

class MarkovRhythmGenerator:
    """Generates rhythmic patterns using Markov chains."""
    
    def __init__(self, seed: int = None):
        if seed:
            np.random.seed(seed)
        # Transition matrix for hit/rest patterns (0=rest, 1=soft, 2=medium, 3=hard)
        self.transition_matrix = np.array([
            [0.3, 0.4, 0.2, 0.1],  # From rest
            [0.4, 0.2, 0.3, 0.1],  # From soft
            [0.3, 0.3, 0.2, 0.2],  # From medium
            [0.5, 0.2, 0.2, 0.1],  # From hard
        ])
    
    def generate_pattern(self, length: int = 16, start_state: int = 0) -> List[int]:
        """Generate a rhythmic pattern using Markov chain."""
        pattern = [start_state]
        current_state = start_state
        
        for _ in range(length - 1):
            probabilities = self.transition_matrix[current_state]
            next_state = np.random.choice(4, p=probabilities)
            pattern.append(next_state)
            current_state = next_state
        
        return pattern

class RandomWalkRhythm:
    """Generates rhythms using random walk algorithm."""
    
    def __init__(self, seed: int = None):
        if seed:
            np.random.seed(seed)
    
    def generate_pattern(self, length: int = 16, min_val: int = 0, max_val: int = 3) -> List[int]:
        """Generate pattern using bounded random walk."""
        pattern = [np.random.randint(min_val, max_val + 1)]
        
        for _ in range(length - 1):
            step = np.random.choice([-1, 0, 1], p=[0.3, 0.4, 0.3])
            new_val = np.clip(pattern[-1] + step, min_val, max_val)
            pattern.append(int(new_val))
        
        return pattern

class FractalRhythm:
    """Generates self-similar rhythmic patterns using fractal subdivision."""
    
    def __init__(self, seed: int = None):
        if seed:
            np.random.seed(seed)
    
    def generate_pattern(self, depth: int = 4) -> List[int]:
        """Generate fractal rhythm pattern."""
        pattern = [2]  # Start with medium hit
        
        for _ in range(depth):
            new_pattern = []
            for val in pattern:
                if np.random.random() < 0.6:
                    # Subdivide
                    variation = np.random.randint(-1, 2)
                    new_pattern.extend([val, max(0, min(3, val + variation))])
                else:
                    new_pattern.extend([val, 0])  # Add rest
            pattern = new_pattern
        
        return pattern[:16]  # Trim to 16 steps

class DrumPatternGenerator:
    """Combines all rhythm generators for complete drum patterns."""
    
    def __init__(self, seed: int = None):
        self.markov = MarkovRhythmGenerator(seed)
        self.random_walk = RandomWalkRhythm(seed)
        self.fractal = FractalRhythm(seed)
    
    def generate_kick_pattern(self, bars: int = 4) -> List[Tuple[float, int]]:
        """Generate kick drum pattern. Returns list of (beat_position, velocity)."""
        pattern = self.markov.generate_pattern(16 * bars)
        events = []
        for i, val in enumerate(pattern):
            if val > 0 and i % 4 == 0:  # Kick on downbeats
                velocity = 60 + val * 20
                events.append((i * 0.25, velocity))
        return events
    
    def generate_hihat_pattern(self, bars: int = 4) -> List[Tuple[float, int]]:
        """Generate hi-hat pattern with random walk dynamics."""
        pattern = self.random_walk.generate_pattern(16 * bars)
        events = []
        for i, val in enumerate(pattern):
            if val > 0:
                velocity = 40 + val * 15
                events.append((i * 0.25, velocity))
        return events
    
    def generate_snare_pattern(self, bars: int = 4) -> List[Tuple[float, int]]:
        """Generate snare pattern using fractal rhythm."""
        base_pattern = self.fractal.generate_pattern(4)
        events = []
        for bar in range(bars):
            for i, val in enumerate(base_pattern):
                if val > 1 and (i == 4 or i == 12):  # Snare on 2 and 4
                    velocity = 70 + val * 15
                    events.append((bar * 4 + i * 0.25, velocity))
        return events
