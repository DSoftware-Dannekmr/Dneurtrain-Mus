"""
A Dawn - Multitrack MIDI Composition
Main composition script that generates the complete piece.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from midiutil import MIDIFile
import numpy as np
from rhythm_generator import DrumPatternGenerator
from bass_generator import BassLineGenerator
from piano_composer import PianoComposer

# Composition parameters
TEMPO = 72  # BPM - slow, contemplative
TIME_SIGNATURE = (4, 4)

# Structure timing (in bars)
STRUCTURE = {
    'intro': (0, 16),        # 0:00 - 0:53 (solo piano)
    'development': (16, 32), # 0:53 - 1:46 (bass enters, then drums)
    'climax': (32, 48),      # 1:46 - 2:40 (full ensemble)
    'ending': (48, 56),      # 2:40 - 3:07 (fade out)
}

def create_piano_track(midi: MIDIFile, track: int, composer: PianoComposer):
    """Create the piano track with all sections."""
    channel = 0
    midi.addProgramChange(track, channel, 0, 0)  # Acoustic Grand Piano
    
    # INTRO - Solo piano, delicate arpeggios and melody
    print("  Composing piano intro...")
    for bar in range(16):
        chord_idx = bar % 4
        chord = composer.PROGRESSIONS['intro'][chord_idx]
        
        # Arpeggios in left hand
        arp = composer.generate_arpeggio(chord, 4, (40, 55))
        for beat, note, vel, dur in arp:
            midi.addNote(track, channel, note - 12, bar * 4 + beat, dur, vel)
        
        # Sparse melody in right hand
        if bar % 2 == 0:
            melody = composer.generate_melody(2, 72)
            for beat, note, vel, dur in melody:
                if beat < 8:
                    midi.addNote(track, channel, note, bar * 4 + beat, dur, vel)
    
    # DEVELOPMENT - More active piano
    print("  Composing piano development...")
    for bar in range(16, 32):
        local_bar = bar - 16
        chord_idx = local_bar % 4
        chord = composer.PROGRESSIONS['development'][chord_idx]
        
        # Fuller arpeggios
        arp = composer.generate_arpeggio(chord, 4, (50, 70))
        for beat, note, vel, dur in arp:
            midi.addNote(track, channel, note - 12, bar * 4 + beat, dur, vel)
        
        # More continuous melody
        melody = composer.generate_melody(1, 74)
        for beat, note, vel, dur in melody:
            midi.addNote(track, channel, note, bar * 4 + beat, dur, min(vel + 10, 100))
    
    # CLIMAX - Expressive, full piano
    print("  Composing piano climax...")
    for bar in range(32, 48):
        local_bar = bar - 32
        chord_idx = local_bar % 8
        chord = composer.PROGRESSIONS['climax'][chord_idx]
        
        # Chord hits on downbeats
        if local_bar % 2 == 0:
            hits = composer.generate_chord_hits(chord, 0, 75)
            for beat, note, vel, dur in hits:
                midi.addNote(track, channel, note, bar * 4 + beat, dur, vel)
        
        # Active arpeggios
        arp = composer.generate_arpeggio(chord, 4, (60, 85))
        for beat, note, vel, dur in arp:
            midi.addNote(track, channel, note - 12, bar * 4 + beat, dur, vel)
        
        # Soaring melody
        melody = composer.generate_melody(1, 76)
        for beat, note, vel, dur in melody:
            midi.addNote(track, channel, note, bar * 4 + beat, dur, min(vel + 15, 110))
    
    # ENDING - Fade out with piano
    print("  Composing piano ending...")
    for bar in range(48, 56):
        local_bar = bar - 48
        chord_idx = local_bar % 4
        chord = composer.PROGRESSIONS['ending'][chord_idx]
        
        # Decreasing velocity for fade
        fade_factor = 1.0 - (local_bar / 8) * 0.6
        
        arp = composer.generate_arpeggio(chord, 4, (int(40 * fade_factor), int(60 * fade_factor)))
        for beat, note, vel, dur in arp:
            midi.addNote(track, channel, note - 12, bar * 4 + beat, dur, max(vel, 20))
        
        if local_bar < 4:
            melody = composer.generate_melody(1, 72)
            for beat, note, vel, dur in melody:
                midi.addNote(track, channel, note, bar * 4 + beat, dur, int(vel * fade_factor))

def create_bass_track(midi: MIDIFile, track: int, generator: BassLineGenerator):
    """Create the bass track (enters in development)."""
    channel = 1
    midi.addProgramChange(track, channel, 0, 33)  # Electric Bass (finger)
    
    # DEVELOPMENT - Bass enters gradually
    print("  Composing bass development...")
    for bar in range(16, 32):
        local_bar = bar - 16
        
        # Gradual velocity increase
        vel_boost = min(local_bar * 2, 20)
        
        events = generator.generate_section('development', 1)
        for beat, note, vel, dur in events:
            midi.addNote(track, channel, note, bar * 4 + beat, dur, min(vel + vel_boost, 100))
    
    # CLIMAX - Full bass
    print("  Composing bass climax...")
    for bar in range(32, 48):
        events = generator.generate_section('climax', 1)
        for beat, note, vel, dur in events:
            midi.addNote(track, channel, note, bar * 4 + beat, dur, vel + 10)
    
    # ENDING - Bass fades
    print("  Composing bass ending...")
    for bar in range(48, 52):  # Bass exits before piano
        local_bar = bar - 48
        fade_factor = 1.0 - (local_bar / 4) * 0.7
        
        events = generator.generate_section('ending', 1)
        for beat, note, vel, dur in events:
            midi.addNote(track, channel, note, bar * 4 + beat, dur, int(vel * fade_factor))


def create_drums_track(midi: MIDIFile, track: int, generator: DrumPatternGenerator):
    """Create the drums track (enters mid-development)."""
    channel = 9  # Standard MIDI drum channel
    
    # GM Drum map
    KICK = 36
    SNARE = 38
    HIHAT_CLOSED = 42
    HIHAT_OPEN = 46
    RIDE = 51
    
    # DEVELOPMENT - Drums enter at bar 24 (light)
    print("  Composing drums development...")
    for bar in range(24, 32):
        local_bar = bar - 24
        vel_factor = 0.5 + (local_bar / 16)  # Gradual increase
        
        # Light hi-hat pattern
        hihat = generator.generate_hihat_pattern(1)
        for beat, vel in hihat:
            midi.addNote(track, channel, HIHAT_CLOSED, bar * 4 + beat, 0.25, int(vel * vel_factor))
        
        # Sparse kick
        if local_bar % 2 == 0:
            kick = generator.generate_kick_pattern(1)
            for beat, vel in kick:
                midi.addNote(track, channel, KICK, bar * 4 + beat, 0.5, int(vel * vel_factor))
    
    # CLIMAX - Full drums
    print("  Composing drums climax...")
    for bar in range(32, 48):
        # Full kick pattern
        kick = generator.generate_kick_pattern(1)
        for beat, vel in kick:
            midi.addNote(track, channel, KICK, bar * 4 + beat, 0.5, vel)
        
        # Snare on 2 and 4
        snare = generator.generate_snare_pattern(1)
        for beat, vel in snare:
            midi.addNote(track, channel, SNARE, bar * 4 + beat, 0.25, vel)
        
        # Active hi-hat
        hihat = generator.generate_hihat_pattern(1)
        for beat, vel in hihat:
            midi.addNote(track, channel, HIHAT_CLOSED, bar * 4 + beat, 0.25, vel)
        
        # Occasional ride
        if bar % 4 == 0:
            midi.addNote(track, channel, RIDE, bar * 4, 1.0, 60)
    
    # ENDING - Drums fade quickly
    print("  Composing drums ending...")
    for bar in range(48, 50):  # Drums exit early
        fade_factor = 1.0 - ((bar - 48) / 2) * 0.8
        
        hihat = generator.generate_hihat_pattern(1)
        for beat, vel in hihat:
            midi.addNote(track, channel, HIHAT_CLOSED, bar * 4 + beat, 0.25, int(vel * fade_factor))

def main():
    """Main composition function."""
    print("=" * 50)
    print("A DAWN - Multitrack MIDI Composition")
    print("=" * 50)
    
    # Initialize generators with seed for reproducibility
    seed = 42
    np.random.seed(seed)
    
    print("\nInitializing generators...")
    piano_composer = PianoComposer(seed)
    bass_generator = BassLineGenerator(seed + 1)
    drum_generator = DrumPatternGenerator(seed + 2)
    
    # Create MIDI file with 3 tracks
    midi = MIDIFile(3, deinterleave=False)
    
    # Set tempo and time signature
    midi.addTempo(0, 0, TEMPO)
    midi.addTimeSignature(0, 0, 4, 2, 24, 8)  # 4/4 time
    
    # Track names
    midi.addTrackName(0, 0, "Piano")
    midi.addTrackName(1, 0, "Bass")
    midi.addTrackName(2, 0, "Drums")
    
    print("\nComposing tracks...")
    
    # Generate each track
    print("\n[Track 1: Piano]")
    create_piano_track(midi, 0, piano_composer)
    
    print("\n[Track 2: Bass]")
    create_bass_track(midi, 1, bass_generator)
    
    print("\n[Track 3: Drums]")
    create_drums_track(midi, 2, drum_generator)
    
    # Write output file
    output_file = "A_Dawn_Multitrack.mid"
    print(f"\nWriting MIDI file: {output_file}")
    
    with open(output_file, "wb") as f:
        midi.writeFile(f)
    
    print("\n" + "=" * 50)
    print("Composition complete!")
    print(f"Duration: ~{56 * 4 / TEMPO:.1f} minutes at {TEMPO} BPM")
    print("Tracks: Piano, Bass, Drums")
    print("=" * 50)
    
    return output_file

if __name__ == "__main__":
    main()
