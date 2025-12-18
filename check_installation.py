#!/usr/bin/env python3
"""
Installation Checker
Verify that all required dependencies are installed
"""
import sys

def check_dependency(name, import_name=None):
    """Check if a dependency is installed"""
    if import_name is None:
        import_name = name
    
    try:
        __import__(import_name)
        print(f"✓ {name:20} installed")
        return True
    except ImportError:
        print(f"✗ {name:20} NOT installed")
        return False

def main():
    print("\n" + "="*60)
    print("Universal Genre MIDI Composer - Installation Check")
    print("="*60 + "\n")
    
    print("Python Version:", sys.version.split()[0])
    print()
    
    # Check required dependencies
    print("REQUIRED DEPENDENCIES:")
    print("-" * 60)
    required = [
        ("midiutil", "midiutil"),
        ("numpy", "numpy"),
        ("mido", "mido"),
    ]
    
    required_ok = all(check_dependency(name, imp) for name, imp in required)
    
    print()
    print("OPTIONAL DEPENDENCIES (for neural features):")
    print("-" * 60)
    optional = [
        ("TensorFlow", "tensorflow"),
        ("Keras", "keras"),
    ]
    
    optional_ok = all(check_dependency(name, imp) for name, imp in optional)
    
    print()
    print("="*60)
    
    if required_ok:
        print("✓ All required dependencies installed!")
        print("  You can use the basic features.")
        
        if optional_ok:
            print("✓ All optional dependencies installed!")
            print("  You can use neural network features.")
        else:
            print("⚠ Optional dependencies missing.")
            print("  Install TensorFlow for neural features:")
            print("  pip install tensorflow")
    else:
        print("✗ Missing required dependencies!")
        print("  Install them with:")
        print("  pip install midiutil numpy mido")
        print()
        print("  For neural features, also install:")
        print("  pip install tensorflow")
        sys.exit(1)
    
    print("="*60 + "\n")
    
    # Try importing main modules
    print("CHECKING MAIN MODULES:")
    print("-" * 60)
    
    try:
        from genres.all_genres import get_genre_count
        count = get_genre_count()
        print(f"✓ Genres module:       {count} genres loaded")
    except Exception as e:
        print(f"✗ Genres module:       Error - {e}")
    
    try:
        from universal_composer import GenreComposer
        print(f"✓ Universal Composer:  Ready")
    except Exception as e:
        print(f"✗ Universal Composer:  Error - {e}")
    
    try:
        from advanced_neural_network import AdvancedNeuralComposer
        print(f"✓ Neural Network:      Ready")
    except Exception as e:
        print(f"✗ Neural Network:      Error - {e}")
    
    print()
    print("="*60)
    print("✓ Installation check complete!")
    print("="*60 + "\n")
    
    print("NEXT STEPS:")
    print("-" * 60)
    print("1. Read NEURAL_QUICK_START.md")
    print("2. Create training_data/ folder")
    print("3. Add MIDI files to training_data/")
    print("4. Run: python train_neural.py")
    print("5. Or start web server: python web_server.py")
    print()

if __name__ == "__main__":
    main()
