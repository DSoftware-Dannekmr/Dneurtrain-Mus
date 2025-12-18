"""
Universal Genre-Based MIDI Composer
Generates music in any genre from the database.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass

from genres.all_genres import (
    ALL_GENRES, get_genre, list_genres, list_genres_by_category,
    search_genres, get_genre_count, get_categories
)
from genres.genre_database import (
    GenreParams, ScaleType, TimeSignature, SCALE_INTERVALS, get_scale_notes
)

try:
    from advanced_neural_network import AdvancedNeuralComposer, EnhancedComposer, MIDIDataProcessor
    NEURAL_AVAILABLE = True
except ImportError:
    NEURAL_AVAILABLE = False
    AdvancedNeuralComposer = None
    EnhancedComposer = None
    MIDIDataProcessor = None

@dataclass
class Note:
    """Represents a MIDI note event."""
    pitch: int
    velocity: int
    start: float  # In beats
    duration: float

class GenreComposer:
    """Composes music based on genre parameters."""
    
    def __init__(self, genre_id: str, seed: int = None, neural_model: Optional['AdvancedNeuralComposer'] = None):
        self.genre = get_genre(genre_id)
        if not self.genre:
            raise ValueError(f"Unknown genre: {genre_id}. Use list_genres() to see available genres.")
        
        if seed:
            np.random.seed(seed)
        
        self.root_note = 60  # Middle C
        self.current_scale = self._get_scale()
        self.neural_model = neural_model
        self.enhanced_composer = EnhancedComposer(neural_model) if NEURAL_AVAILABLE and neural_model else None
    
    def _get_scale(self) -> List[int]:
        """Get scale notes based on genre's preferred scales."""
        scale_type = np.random.choice(self.genre.scales)
        return get_scale_notes(self.root_note, scale_type)
    
    def _get_tempo(self) -> int:
        """Get random tempo within genre's range."""
        return np.random.randint(self.genre.tempo_range[0], self.genre.tempo_range[1] + 1)
    
    def _get_time_signature(self) -> Tuple[int, int]:
        """Get random time signature from genre's options."""
        ts = np.random.choice(self.genre.time_signatures)
        return ts.value
    
    def _apply_swing(self, beat: float) -> float:
        """Apply swing feel to beat position."""
        if self.genre.swing == 0:
            return beat
        
        beat_in_pair = beat % 1.0
        if beat_in_pair >= 0.5:
            # Delay the off-beat
            delay = self.genre.swing * 0.15
            return beat + delay
        return beat
    
    def _get_velocity(self) -> int:
        """Get random velocity within genre's range."""
        return np.random.randint(self.genre.velocity_range[0], self.genre.velocity_range[1] + 1)
    
    def _snap_to_scale(self, note: int) -> int:
        """Snap note to nearest scale degree."""
        octave = (note // 12) * 12
        pitch_class = note % 12
        scale_pcs = [n % 12 for n in self.current_scale]
        closest = min(scale_pcs, key=lambda x: min(abs(x - pitch_class), 12 - abs(x - pitch_class)))
        return octave + closest
    
    def generate_melody(self, bars: int = 4) -> List[Note]:
        """Generate a melodic line."""
        notes = []
        time_sig = self._get_time_signature()
        beats_per_bar = time_sig[0]
        total_beats = bars * beats_per_bar
        
        current_beat = 0.0
        prev_note = np.random.choice(self.current_scale)
        
        while current_beat < total_beats:
            # Determine note duration based on density
            if self.genre.note_density > 0.7:
                durations = [0.25, 0.5]
            elif self.genre.note_density > 0.4:
                durations = [0.5, 1.0, 0.25]
            else:
                durations = [1.0, 2.0, 0.5]
            
            duration = np.random.choice(durations)
            
            # Generate note with melodic contour
            if np.random.random() < 0.7:
                # Step motion
                step = np.random.choice([-2, -1, 0, 1, 2])
                scale_idx = self.current_scale.index(self._snap_to_scale(prev_note))
                new_idx = max(0, min(len(self.current_scale) - 1, scale_idx + step))
                pitch = self.current_scale[new_idx]
            else:
                # Leap
                pitch = np.random.choice(self.current_scale)
            
            # Apply syncopation
            beat = current_beat
            if np.random.random() < self.genre.syncopation:
                beat += np.random.choice([0.25, -0.25, 0.5])
                beat = max(0, beat)
            
            beat = self._apply_swing(beat)
            velocity = self._get_velocity()
            
            notes.append(Note(pitch, velocity, beat, duration))
            prev_note = pitch
            current_beat += duration
        
        # Enhance with neural network if available
        if self.enhanced_composer and NEURAL_AVAILABLE:
            try:
                notes = self.enhanced_composer.enhance_melody(notes)
            except Exception as e:
                # If neural enhancement fails, use original notes
                pass
        
        return notes
    
    def generate_bass_line(self, bars: int = 4, chord_roots: List[int] = None) -> List[Note]:
        """Generate a bass line."""
        notes = []
        time_sig = self._get_time_signature()
        beats_per_bar = time_sig[0]
        
        if chord_roots is None:
            # Default chord progression
            chord_roots = [self.root_note - 12, self.root_note - 7, 
                          self.root_note - 5, self.root_note - 12]
        
        for bar in range(bars):
            root = chord_roots[bar % len(chord_roots)]
            
            # Bass pattern based on genre style
            if self.genre.bass_style in ["walking", "walking_swing", "blues_walking"]:
                # Walking bass
                for beat in range(beats_per_bar):
                    if beat == 0:
                        pitch = root
                    elif beat == beats_per_bar - 1:
                        # Approach note
                        next_root = chord_roots[(bar + 1) % len(chord_roots)]
                        pitch = next_root + np.random.choice([-1, 1])
                    else:
                        pitch = root + np.random.choice([0, 5, 7, 12])
                    
                    notes.append(Note(pitch, self._get_velocity(), bar * beats_per_bar + beat, 1.0))
            
            elif self.genre.bass_style in ["root_fifth", "root_power"]:
                # Root-fifth pattern
                notes.append(Note(root, self._get_velocity(), bar * beats_per_bar, 2.0))
                notes.append(Note(root + 7, self._get_velocity(), bar * beats_per_bar + 2, 2.0))
            
            elif self.genre.bass_style in ["808_bass", "trap", "drill_bass"]:
                # 808 style - long sustained notes with slides
                notes.append(Note(root, self._get_velocity(), bar * beats_per_bar, beats_per_bar))
            
            elif self.genre.bass_style in ["tumbao", "salsa_bass"]:
                # Latin tumbao pattern
                pattern = [0, 0.5, 2.5, 3]
                for beat in pattern:
                    pitch = root if beat in [0, 2.5] else root + 7
                    notes.append(Note(pitch, self._get_velocity(), bar * beats_per_bar + beat, 0.5))
            
            else:
                # Default: root on downbeats
                for beat in range(0, beats_per_bar, 2):
                    notes.append(Note(root, self._get_velocity(), bar * beats_per_bar + beat, 2.0))
        
        # Enhance with neural network if available
        if self.enhanced_composer and NEURAL_AVAILABLE:
            try:
                notes = self.enhanced_composer.enhance_melody(notes)
            except Exception as e:
                # If neural enhancement fails, use original notes
                pass
        
        return notes
    
    def generate_chords(self, bars: int = 4) -> List[List[Note]]:
        """Generate chord progression."""
        chords = []
        time_sig = self._get_time_signature()
        beats_per_bar = time_sig[0]
        
        # Common chord progressions based on complexity
        if self.genre.chord_complexity < 0.3:
            # Simple: I-IV-V-I
            progression = [[0, 4, 7], [5, 9, 12], [7, 11, 14], [0, 4, 7]]
        elif self.genre.chord_complexity < 0.6:
            # Medium: I-vi-IV-V
            progression = [[0, 4, 7], [9, 12, 16], [5, 9, 12], [7, 11, 14]]
        else:
            # Complex: jazz-style with extensions
            progression = [[0, 4, 7, 11], [5, 9, 12, 16], [7, 11, 14, 17], [0, 4, 7, 10]]
        
        for bar in range(bars):
            chord_intervals = progression[bar % len(progression)]
            bar_chords = []
            
            for interval in chord_intervals:
                pitch = self.root_note + interval
                velocity = self._get_velocity() - 10  # Slightly softer than melody
                bar_chords.append(Note(pitch, velocity, bar * beats_per_bar, beats_per_bar))
            
            chords.append(bar_chords)
        
        return chords
    
    def generate_drum_pattern(self, bars: int = 4) -> dict:
        """Generate drum pattern based on genre."""
        time_sig = self._get_time_signature()
        beats_per_bar = time_sig[0]
        
        # GM Drum map
        KICK = 36
        SNARE = 38
        HIHAT_CLOSED = 42
        HIHAT_OPEN = 46
        RIDE = 51
        CRASH = 49
        TOM_HIGH = 50
        TOM_LOW = 45
        
        drums = {"kick": [], "snare": [], "hihat": [], "other": []}
        
        for bar in range(bars):
            bar_start = bar * beats_per_bar
            
            # Pattern varies by genre
            if self.genre.drum_pattern in ["four_on_floor", "house", "techno"]:
                # Four on the floor
                for beat in range(beats_per_bar):
                    drums["kick"].append(Note(KICK, self._get_velocity(), bar_start + beat, 0.5))
                    if beat % 2 == 1:
                        drums["snare"].append(Note(SNARE, self._get_velocity(), bar_start + beat, 0.5))
                    drums["hihat"].append(Note(HIHAT_CLOSED, self._get_velocity() - 20, bar_start + beat, 0.25))
                    drums["hihat"].append(Note(HIHAT_CLOSED, self._get_velocity() - 30, bar_start + beat + 0.5, 0.25))
            
            elif self.genre.drum_pattern in ["rock_basic", "rock_heavy"]:
                # Rock beat
                drums["kick"].append(Note(KICK, self._get_velocity(), bar_start, 0.5))
                drums["kick"].append(Note(KICK, self._get_velocity(), bar_start + 2.5, 0.5))
                drums["snare"].append(Note(SNARE, self._get_velocity(), bar_start + 1, 0.5))
                drums["snare"].append(Note(SNARE, self._get_velocity(), bar_start + 3, 0.5))
                for i in range(8):
                    drums["hihat"].append(Note(HIHAT_CLOSED, self._get_velocity() - 20, bar_start + i * 0.5, 0.25))
            
            elif self.genre.drum_pattern in ["trap", "drill"]:
                # Trap pattern with hi-hat rolls
                drums["kick"].append(Note(KICK, self._get_velocity(), bar_start, 1.0))
                drums["kick"].append(Note(KICK, self._get_velocity(), bar_start + 2.25, 0.5))
                drums["snare"].append(Note(SNARE, self._get_velocity(), bar_start + 1, 0.5))
                drums["snare"].append(Note(SNARE, self._get_velocity(), bar_start + 3, 0.5))
                # Hi-hat rolls
                for i in range(16):
                    vel = self._get_velocity() - 30 + np.random.randint(-10, 10)
                    drums["hihat"].append(Note(HIHAT_CLOSED, vel, bar_start + i * 0.25, 0.125))
            
            elif self.genre.drum_pattern in ["boom_bap", "hip_hop"]:
                # Boom bap
                drums["kick"].append(Note(KICK, self._get_velocity(), bar_start, 0.5))
                drums["kick"].append(Note(KICK, self._get_velocity(), bar_start + 2.5, 0.5))
                drums["snare"].append(Note(SNARE, self._get_velocity(), bar_start + 1, 0.5))
                drums["snare"].append(Note(SNARE, self._get_velocity(), bar_start + 3.25, 0.5))
                for i in range(4):
                    drums["hihat"].append(Note(HIHAT_CLOSED, self._get_velocity() - 20, bar_start + i, 0.5))
            
            elif self.genre.drum_pattern in ["jazz", "bebop", "swing"]:
                # Jazz ride pattern
                for beat in range(beats_per_bar):
                    drums["other"].append(Note(RIDE, self._get_velocity() - 10, bar_start + beat, 0.5))
                    if np.random.random() < 0.5:
                        drums["other"].append(Note(RIDE, self._get_velocity() - 20, bar_start + beat + 0.66, 0.25))
                # Kick and snare comping
                if np.random.random() < 0.3:
                    drums["kick"].append(Note(KICK, self._get_velocity() - 20, bar_start + np.random.choice([0, 2]), 0.5))
            
            elif self.genre.drum_pattern in ["salsa_clave", "latin_clave"]:
                # Son clave 3-2
                clave_pattern = [0, 1.5, 2.5] if bar % 2 == 0 else [1, 2]
                for beat in clave_pattern:
                    drums["other"].append(Note(76, self._get_velocity(), bar_start + beat, 0.25))  # Woodblock
                # Tumbao kick
                drums["kick"].append(Note(KICK, self._get_velocity(), bar_start + 2.5, 0.5))
            
            elif self.genre.drum_pattern in ["reggae", "one_drop"]:
                # One drop
                drums["snare"].append(Note(SNARE, self._get_velocity(), bar_start + 2, 0.5))
                drums["kick"].append(Note(KICK, self._get_velocity(), bar_start + 2, 0.5))
                for i in range(8):
                    drums["hihat"].append(Note(HIHAT_CLOSED, self._get_velocity() - 20, bar_start + i * 0.5, 0.25))
            
            elif self.genre.drum_pattern == "none":
                # No drums
                pass
            
            else:
                # Default pattern
                drums["kick"].append(Note(KICK, self._get_velocity(), bar_start, 0.5))
                drums["kick"].append(Note(KICK, self._get_velocity(), bar_start + 2, 0.5))
                drums["snare"].append(Note(SNARE, self._get_velocity(), bar_start + 1, 0.5))
                drums["snare"].append(Note(SNARE, self._get_velocity(), bar_start + 3, 0.5))
                for i in range(8):
                    drums["hihat"].append(Note(HIHAT_CLOSED, self._get_velocity() - 20, bar_start + i * 0.5, 0.25))
        
        return drums

def print_genre_info(genre_id: str):
    """Print detailed information about a genre."""
    genre = get_genre(genre_id)
    if not genre:
        print(f"Genre '{genre_id}' not found.")
        return
    
    print(f"\n{'='*50}")
    print(f"Genre: {genre.name}")
    print(f"Category: {genre.category}")
    print(f"{'='*50}")
    print(f"Description: {genre.description}")
    print(f"Tempo: {genre.tempo_range[0]}-{genre.tempo_range[1]} BPM")
    print(f"Time Signatures: {[ts.value for ts in genre.time_signatures]}")
    print(f"Scales: {[s.value for s in genre.scales]}")
    print(f"Swing: {genre.swing}")
    print(f"Velocity Range: {genre.velocity_range}")
    print(f"Note Density: {genre.note_density}")
    print(f"Syncopation: {genre.syncopation}")
    print(f"Chord Complexity: {genre.chord_complexity}")
    print(f"Instruments: {', '.join(genre.instruments)}")
    print(f"Drum Pattern: {genre.drum_pattern}")
    print(f"Bass Style: {genre.bass_style}")

if __name__ == "__main__":
    print(f"Universal Genre Composer")
    print(f"Total genres available: {get_genre_count()}")
    print(f"\nCategories: {', '.join(sorted(get_categories()))}")
    
    # Example: show info for a few genres
    for genre_id in ["trap", "jazz_fusion", "salsa", "soviet_rock"]:
        print_genre_info(genre_id)
