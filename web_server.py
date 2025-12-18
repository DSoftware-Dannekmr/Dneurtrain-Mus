"""
Web Server for Universal Genre MIDI Composer
Provides a web interface for generating MIDI files
"""
import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser
from pathlib import Path
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from midiutil import MIDIFile
    MIDIUTIL_AVAILABLE = True
except ImportError:
    MIDIUTIL_AVAILABLE = False

try:
    from advanced_neural_network import AdvancedNeuralComposer, train_neural_composer
    NEURAL_AVAILABLE = True
except ImportError:
    NEURAL_AVAILABLE = False

import numpy as np
from universal_composer import GenreComposer
from genres.all_genres import (
    get_genre, list_genres, list_genres_by_category,
    search_genres, get_genre_count, get_categories
)

class ComposerHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for the composer"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        # API endpoints
        if path == '/api/genres':
            self.send_json(list_genres())
        
        elif path == '/api/categories':
            self.send_json(list_genres_by_category())
        
        elif path == '/api/genre-info':
            genre_id = query.get('id', [None])[0]
            if genre_id:
                genre = get_genre(genre_id)
                if genre:
                    info = {
                        'id': genre_id,
                        'name': genre.name,
                        'category': genre.category,
                        'description': genre.description,
                        'tempo_range': genre.tempo_range,
                        'scales': [s.value for s in genre.scales],
                        'swing': genre.swing,
                        'velocity_range': genre.velocity_range,
                        'note_density': genre.note_density,
                        'syncopation': genre.syncopation,
                        'instruments': genre.instruments,
                        'drum_pattern': genre.drum_pattern,
                        'bass_style': genre.bass_style,
                        'chord_complexity': genre.chord_complexity,
                    }
                    self.send_json(info)
                else:
                    self.send_error(404, "Genre not found")
            else:
                self.send_error(400, "Missing genre id")
        
        elif path == '/api/search':
            query_str = query.get('q', [''])[0]
            results = search_genres(query_str)
            self.send_json(results)
        
        elif path == '/api/generate':
            genre_id = query.get('genre', [None])[0]
            bars = int(query.get('bars', [32])[0])
            seed = query.get('seed', [None])[0]
            use_neural = query.get('neural', ['false'])[0].lower() == 'true'
            
            if not genre_id:
                self.send_error(400, "Missing genre parameter")
                return
            
            if not MIDIUTIL_AVAILABLE:
                self.send_error(500, "midiutil not installed")
                return
            
            try:
                seed = int(seed) if seed else None
                filename = self.generate_midi(genre_id, bars, seed, use_neural)
                self.send_json({'success': True, 'filename': filename})
            except Exception as e:
                self.send_error(500, str(e))
        
        elif path == '/api/models':
            # List available neural models
            models_dir = 'models'
            models = []
            if os.path.exists(models_dir):
                models = [f for f in os.listdir(models_dir) if f.endswith('.h5')]
            self.send_json({'models': models})
        
        elif path == '/api/model-status':
            # Check if a model is trained
            model_name = query.get('model', ['composer_model'])[0]
            model_path = f'models/{model_name}.h5'
            exists = os.path.exists(model_path)
            self.send_json({'exists': exists, 'model': model_name})
        
        elif path == '/':
            self.send_file('index.html', 'text/html')
        
        elif path.endswith('.html'):
            self.send_file(path[1:], 'text/html')
        
        elif path.endswith('.css'):
            self.send_file(path[1:], 'text/css')
        
        elif path.endswith('.js'):
            self.send_file(path[1:], 'application/javascript')
        
        elif path.endswith('.mid'):
            self.send_file(path[1:], 'audio/midi')
        
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        if path == '/api/generate':
            try:
                data = json.loads(body)
                genre_id = data.get('genre')
                bars = data.get('bars', 32)
                seed = data.get('seed')
                use_neural = data.get('neural', False)
                
                if not genre_id:
                    self.send_error(400, "Missing genre")
                    return
                
                if not MIDIUTIL_AVAILABLE:
                    self.send_error(500, "midiutil not installed")
                    return
                
                filename = self.generate_midi(genre_id, bars, seed, use_neural)
                self.send_json({'success': True, 'filename': filename})
            except Exception as e:
                self.send_error(500, str(e))
        
        elif path == '/api/train-neural':
            if not NEURAL_AVAILABLE:
                self.send_json({'success': False, 'error': 'Neural network not available. Install TensorFlow: pip install tensorflow'})
                return
            
            try:
                data = json.loads(body)
                midi_directory = data.get('directory', 'training_data')
                epochs = data.get('epochs', 50)
                model_name = data.get('model_name', 'composer_model')
                
                # Check if directory exists
                if not os.path.exists(midi_directory):
                    self.send_json({
                        'success': False,
                        'error': f'Directory not found: {midi_directory}. Create the directory and add MIDI files.'
                    })
                    return
                
                # Train model
                composer = train_neural_composer(midi_directory, epochs)
                
                if composer:
                    # Save to models directory
                    os.makedirs('models', exist_ok=True)
                    model_path = f'models/{model_name}.h5'
                    composer.save_model(model_path)
                    
                    self.send_json({
                        'success': True,
                        'message': f'Model trained and saved to {model_path}',
                        'model': model_name
                    })
                else:
                    self.send_json({
                        'success': False,
                        'error': f'No MIDI files found in {midi_directory}. Add .mid or .midi files to the directory.'
                    })
            except Exception as e:
                self.send_json({'success': False, 'error': str(e)})
        
        elif path == '/api/load-model':
            if not NEURAL_AVAILABLE:
                self.send_error(500, "Neural network not available")
                return
            
            try:
                data = json.loads(body)
                model_name = data.get('model', 'composer_model')
                model_path = f'models/{model_name}.h5'
                
                if not os.path.exists(model_path):
                    self.send_error(404, f"Model not found: {model_path}")
                    return
                
                self.send_json({
                    'success': True,
                    'message': f'Model loaded: {model_name}',
                    'model': model_name
                })
            except Exception as e:
                self.send_error(500, str(e))
        
        else:
            self.send_error(404, "Not found")
    
    def generate_midi(self, genre_id, bars, seed, use_neural=False):
        """Generate MIDI file"""
        genre = get_genre(genre_id)
        if not genre:
            raise ValueError(f"Unknown genre: {genre_id}")
        
        # Load neural model if requested
        neural_model = None
        if use_neural and NEURAL_AVAILABLE:
            try:
                model_path = 'models/composer_model.h5'
                if os.path.exists(model_path):
                    neural_model = AdvancedNeuralComposer()
                    neural_model.load_model(model_path)
            except Exception as e:
                print(f"Warning: Could not load neural model: {e}")
        
        composer = GenreComposer(genre_id, seed, neural_model)
        tempo = composer._get_tempo()
        time_sig = composer._get_time_signature()
        
        midi = MIDIFile(4, deinterleave=False)
        midi.addTempo(0, 0, tempo)
        midi.addTimeSignature(0, 0, time_sig[0], int(np.log2(time_sig[1])), 24, 8)
        
        midi.addTrackName(0, 0, "Melody")
        midi.addTrackName(1, 0, "Chords")
        midi.addTrackName(2, 0, "Bass")
        midi.addTrackName(3, 0, "Drums")
        
        # Set instruments
        midi.addProgramChange(0, 0, 0, 0)   # Piano
        midi.addProgramChange(1, 1, 0, 0)   # Piano
        midi.addProgramChange(2, 2, 0, 33)  # Electric Bass
        
        # Generate tracks
        melody = composer.generate_melody(bars)
        for note in melody:
            midi.addNote(0, 0, note.pitch, note.start, note.duration, note.velocity)
        
        chords = composer.generate_chords(bars)
        for bar_chords in chords:
            for note in bar_chords:
                midi.addNote(1, 1, note.pitch, note.start, note.duration, note.velocity)
        
        bass = composer.generate_bass_line(bars)
        for note in bass:
            midi.addNote(2, 2, note.pitch, note.start, note.duration, note.velocity)
        
        drums = composer.generate_drum_pattern(bars)
        for part_name, part_notes in drums.items():
            for note in part_notes:
                midi.addNote(3, 9, note.pitch, note.start, note.duration, note.velocity)
        
        # Save file
        suffix = "_neural" if use_neural else ""
        filename = f"{genre_id}_{bars}bars{suffix}.mid"
        filepath = os.path.join('output', filename)
        os.makedirs('output', exist_ok=True)
        
        with open(filepath, 'wb') as f:
            midi.writeFile(f)
        
        return filename
    
    def send_json(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_file(self, filename, content_type):
        """Send file response"""
        try:
            with open(filename, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def start_server(port=8000):
    """Start the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ComposerHandler)
    
    print(f"\n{'='*60}")
    print(f"Universal Genre MIDI Composer - Web Interface")
    print(f"{'='*60}")
    print(f"\n✓ Server running at: http://localhost:{port}")
    print(f"✓ Open your browser and navigate to the URL above")
    print(f"\nPress Ctrl+C to stop the server\n")
    
    # Open browser automatically
    threading.Timer(1.0, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    
    start_server(port)
