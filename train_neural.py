#!/usr/bin/env python3
"""
Neural Network Training Script
Train the neural composer on MIDI files from a directory
"""
import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from advanced_neural_network import train_neural_composer, AdvancedNeuralComposer
except ImportError:
    print("Error: advanced_neural_network module not found")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Train neural composer on MIDI files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python train_neural.py                          # Train on training_data/ with 50 epochs
  python train_neural.py -d my_midi_files -e 100 # Train on my_midi_files/ with 100 epochs
  python train_neural.py -d jazz_files -m jazz_model -e 200  # Train jazz-specific model
        """
    )
    
    parser.add_argument(
        '-d', '--directory',
        default='training_data',
        help='Directory containing MIDI files (default: training_data)'
    )
    
    parser.add_argument(
        '-e', '--epochs',
        type=int,
        default=50,
        help='Number of training epochs (default: 50)'
    )
    
    parser.add_argument(
        '-m', '--model',
        default='composer_model',
        help='Model name to save (default: composer_model)'
    )
    
    parser.add_argument(
        '-b', '--batch-size',
        type=int,
        default=32,
        help='Batch size for training (default: 32)'
    )
    
    parser.add_argument(
        '-v', '--validation-split',
        type=float,
        default=0.2,
        help='Validation split ratio (default: 0.2)'
    )
    
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='List available trained models'
    )
    
    args = parser.parse_args()
    
    # List models
    if args.list_models:
        print("\n" + "="*60)
        print("Available Trained Models")
        print("="*60)
        
        models_dir = 'models'
        if os.path.exists(models_dir):
            models = [f for f in os.listdir(models_dir) if f.endswith('.h5')]
            if models:
                for i, model in enumerate(models, 1):
                    model_path = os.path.join(models_dir, model)
                    size_mb = os.path.getsize(model_path) / (1024 * 1024)
                    print(f"{i}. {model} ({size_mb:.1f} MB)")
            else:
                print("No trained models found")
        else:
            print("No models directory found")
        
        print("="*60 + "\n")
        return
    
    # Validate directory
    if not os.path.exists(args.directory):
        print(f"\n❌ Error: Directory '{args.directory}' not found")
        print(f"Please create the directory and add MIDI files to it")
        sys.exit(1)
    
    midi_files = list(Path(args.directory).glob('**/*.mid')) + \
                 list(Path(args.directory).glob('**/*.midi'))
    
    if not midi_files:
        print(f"\n❌ Error: No MIDI files found in '{args.directory}'")
        print(f"Please add .mid or .midi files to the directory")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("Neural Composer Training")
    print("="*60)
    print(f"Directory: {args.directory}")
    print(f"MIDI Files: {len(midi_files)}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch Size: {args.batch_size}")
    print(f"Validation Split: {args.validation_split}")
    print(f"Model Name: {args.model}")
    print("="*60 + "\n")
    
    # Train
    try:
        print("Starting training...\n")
        composer = train_neural_composer(
            args.directory,
            epochs=args.epochs
        )
        
        if composer:
            # Save model
            os.makedirs('models', exist_ok=True)
            model_path = f'models/{args.model}.h5'
            composer.save_model(model_path)
            
            print("\n" + "="*60)
            print("✓ Training Complete!")
            print("="*60)
            print(f"Model saved to: {model_path}")
            print(f"\nYou can now use this model to generate music:")
            print(f"  - Via web interface: Check 'Usar Red Neuronal' checkbox")
            print(f"  - Via Python: neural_model.load_model('{model_path}')")
            print("="*60 + "\n")
        else:
            print("\n❌ Training failed")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠ Training interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
