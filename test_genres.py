"""
Test script to verify all genres load correctly
"""
import sys
import os

try:
    from genres.all_genres import (
        get_genre_count, get_categories, list_genres_by_category,
        search_genres, get_genre
    )
    
    print("✓ Genres module loaded successfully\n")
    
    # Print summary
    total = get_genre_count()
    categories = get_categories()
    
    print(f"Total genres: {total}")
    print(f"Total categories: {len(categories)}\n")
    
    # Print by category
    print("Genres by category:")
    print("-" * 50)
    
    by_cat = list_genres_by_category()
    for cat in sorted(by_cat.keys()):
        count = len(by_cat[cat])
        print(f"  {cat}: {count} genres")
    
    print("\n" + "=" * 50)
    print("Sample genres:")
    print("=" * 50)
    
    samples = ["trap", "jazz_fusion", "salsa", "soviet_rock", "flamenco", "ambient"]
    for genre_id in samples:
        genre = get_genre(genre_id)
        if genre:
            print(f"\n{genre_id}:")
            print(f"  Name: {genre.name}")
            print(f"  Category: {genre.category}")
            print(f"  Tempo: {genre.tempo_range[0]}-{genre.tempo_range[1]} BPM")
            print(f"  Description: {genre.description}")
        else:
            print(f"\n{genre_id}: NOT FOUND")
    
    print("\n" + "=" * 50)
    print("✓ All tests passed!")
    print("=" * 50)
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
