"""
Generate MIDI in Any Genre
Main script to create multitrack MIDI files in any musical genre.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from midiutil import MIDIFile
    MIDIUTIL_AVAILABLE = True
except ImportError:
    MIDIUTIL_AVAILABLE = False
    print("Warning: midiutil not installed. Run: pip install midiutil")

import numpy as np
from universal_composer import GenreComposer, Note, print_genre_info
from genres.all_genres import (
    get_genre, list_genres, list_genres_by_category,
    search_genres, get_genre_count, get_categories
)

def generate_midi(genre_id: str, output_file: str = None, bars: int = 32, seed: int = None):
    """
    Generate a multitrack MIDI file in the specified genre.
    
    Args:
        genre_id: Genre identifier (use list_genres() to see options)
        output_file: Output filename (default: {genre_id}.mid)
        bars: Number of bars to generate
        seed: Random seed for reproducibility
    """
    if not MIDIUTIL_AVAILABLE:
        print("Error: midiutil is required. Install with: pip install midiutil")
        return None
    
    genre = get_genre(genre_id)
    if not genre:
        print(f"Error: Unknown genre '{genre_id}'")
        print(f"Available genres: {', '.join(list_genres()[:20])}...")
        return None
    
    if output_file is None:
        output_file = f"{genre_id}.mid"
    
    print(f"\n{'='*60}")
    print(f"Generating: {genre.name}")
    print(f"Category: {genre.category}")
    print(f"Description: {genre.description}")
    print(f"{'='*60}")
    
    # Initialize composer
    composer = GenreComposer(genre_id, seed)
    tempo = composer._get_tempo()
    time_sig = composer._get_time_signature()
    
    print(f"Tempo: {tempo} BPM")
    print(f"Time Signature: {time_sig[0]}/{time_sig[1]}")
    print(f"Bars: {bars}")
    
    # Create MIDI file with 4 tracks
    midi = MIDIFile(4, deinterleave=False)
    
    # Set tempo and time signature
    midi.addTempo(0, 0, tempo)
    midi.addTimeSignature(0, 0, time_sig[0], int(np.log2(time_sig[1])), 24, 8)
    
    # Track names
    midi.addTrackName(0, 0, "Melody")
    midi.addTrackName(1, 0, "Chords")
    midi.addTrackName(2, 0, "Bass")
    midi.addTrackName(3, 0, "Drums")
    
    # Set instruments based on genre
    # Track 0: Melody
    if "guitar" in genre.instruments[0] if genre.instruments else False:
        midi.addProgramChange(0, 0, 0, 25)  # Acoustic Guitar
    elif "synth" in str(genre.instruments):
        midi.addProgramChange(0, 0, 0, 81)  # Lead Synth
    elif "saxophone" in str(genre.instruments):
        midi.addProgramChange(0, 0, 0, 66)  # Tenor Sax
    elif "violin" in str(genre.instruments):
        midi.addProgramChange(0, 0, 0, 40)  # Violin
    else:
        midi.addProgramChange(0, 0, 0, 0)   # Piano
    
    # Track 1: Chords
    if "organ" in str(genre.instruments):
        midi.addProgramChange(1, 1, 0, 16)  # Organ
    elif "synth" in str(genre.instruments):
        midi.addProgramChange(1, 1, 0, 89)  # Pad
    else:
        midi.addProgramChange(1, 1, 0, 0)   # Piano
    
    # Track 2: Bass
    if "808" in genre.bass_style or "trap" in genre.bass_style:
        midi.addProgramChange(2, 2, 0, 38)  # Synth Bass
    elif "synth" in genre.bass_style:
        midi.addProgramChange(2, 2, 0, 38)  # Synth Bass
    else:
        midi.addProgramChange(2, 2, 0, 33)  # Electric Bass
    
    # Generate content
    print("\nGenerating tracks...")
    
    # Melody
    print("  [1/4] Melody...")
    melody = composer.generate_melody(bars)
    for note in melody:
        midi.addNote(0, 0, note.pitch, note.start, note.duration, note.velocity)
    
    # Chords
    print("  [2/4] Chords...")
    chords = composer.generate_chords(bars)
    for bar_chords in chords:
        for note in bar_chords:
            midi.addNote(1, 1, note.pitch, note.start, note.duration, note.velocity)
    
    # Bass
    print("  [3/4] Bass...")
    bass = composer.generate_bass_line(bars)
    for note in bass:
        midi.addNote(2, 2, note.pitch, note.start, note.duration, note.velocity)
    
    # Drums
    print("  [4/4] Drums...")
    drums = composer.generate_drum_pattern(bars)
    for part_name, part_notes in drums.items():
        for note in part_notes:
            midi.addNote(3, 9, note.pitch, note.start, note.duration, note.velocity)
    
    # Write file
    print(f"\nWriting: {output_file}")
    with open(output_file, "wb") as f:
        midi.writeFile(f)
    
    # Calculate duration
    beats_per_bar = time_sig[0]
    total_beats = bars * beats_per_bar
    duration_seconds = total_beats * 60 / tempo
    duration_minutes = duration_seconds / 60
    
    print(f"\n{'='*60}")
    print(f"✓ Generated: {output_file}")
    print(f"  Duration: {duration_minutes:.1f} minutes ({duration_seconds:.0f} seconds)")
    print(f"  Tracks: Melody, Chords, Bass, Drums")
    print(f"{'='*60}")
    
    return output_file

def list_all_genres():
    """Print all available genres organized by category."""
    print(f"\n{'='*60}")
    print(f"AVAILABLE GENRES ({get_genre_count()} total)")
    print(f"{'='*60}\n")
    
    by_category = list_genres_by_category()
    for category in sorted(by_category.keys()):
        genres = by_category[category]
        print(f"\n{category.upper()} ({len(genres)} genres)")
        print("-" * 40)
        for genre_id in sorted(genres):
            genre = get_genre(genre_id)
            print(f"  {genre_id}: {genre.name}")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate MIDI in any musical genre")
    parser.add_argument("genre", nargs="?", help="Genre ID to generate")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument("-b", "--bars", type=int, default=32, help="Number of bars (default: 32)")
    parser.add_argument("-s", "--seed", type=int, help="Random seed")
    parser.add_argument("-l", "--list", action="store_true", help="List all genres")
    parser.add_argument("-i", "--info", help="Show info about a genre")
    parser.add_argument("--search", help="Search genres by keyword")
    
    args = parser.parse_args()
    
    if args.list:
        list_all_genres()
        return
    
    if args.info:
        print_genre_info(args.info)
        return
    
    if args.search:
        results = search_genres(args.search)
        print(f"\nSearch results for '{args.search}':")
        for genre_id in results:
            genre = get_genre(genre_id)
            print(f"  {genre_id}: {genre.name} ({genre.category})")
        return
    
    if not args.genre:
        print("Universal Genre MIDI Composer")
        print(f"Total genres available: {get_genre_count()}")
        print("\nUsage:")
        print("  python generate_any_genre.py <genre_id> [-o output.mid] [-b bars] [-s seed]")
        print("  python generate_any_genre.py --list          # List all genres")
        print("  python generate_any_genre.py --info <genre>  # Show genre info")
        print("  python generate_any_genre.py --search <term> # Search genres")
        print("\nExamples:")
        print("  python generate_any_genre.py trap")
        print("  python generate_any_genre.py jazz_fusion -b 64")
        print("  python generate_any_genre.py salsa -o my_salsa.mid")
        return
    
    generate_midi(args.genre, args.output, args.bars, args.seed)

if __name__ == "__main__":
    main()
