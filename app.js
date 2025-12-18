// Universal Genre MIDI Composer - Frontend App

class ComposerApp {
    constructor() {
        this.genres = [];
        this.categories = {};
        this.selectedGenre = null;
        this.currentCategory = 'all';
        
        this.init();
    }
    
    async init() {
        await this.loadGenres();
        this.setupEventListeners();
        this.renderGenres();
    }
    
    async loadGenres() {
        try {
            const response = await fetch('/api/genres');
            this.genres = await response.json();
            
            const catResponse = await fetch('/api/categories');
            this.categories = await catResponse.json();
        } catch (error) {
            console.error('Error loading genres:', error);
            this.showError('Error al cargar los géneros');
        }
    }
    
    setupEventListeners() {
        // Search
        document.getElementById('searchBtn').addEventListener('click', () => this.search());
        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.search();
        });
        
        // Category tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.selectCategory(e.target.dataset.category));
        });
        
        // Bars input
        document.getElementById('barsInput').addEventListener('input', (e) => {
            document.getElementById('barsDisplay').textContent = e.target.value;
        });
        
        // Random seed
        document.getElementById('randomSeedBtn').addEventListener('click', () => {
            const seed = Math.floor(Math.random() * 10000);
            document.getElementById('seedInput').value = seed;
        });
        
        // Generate button
        document.getElementById('generateBtn').addEventListener('click', () => this.generate());
        
        // Neural network training
        document.getElementById('trainNeuralBtn').addEventListener('click', () => this.trainNeural());
        
        // Check model status on init
        this.checkModelStatus();
    }
    
    renderGenres(genreList = this.genres) {
        const container = document.getElementById('genreList');
        
        if (genreList.length === 0) {
            container.innerHTML = '<div class="loading">No se encontraron géneros</div>';
            return;
        }
        
        container.innerHTML = genreList.map(genreId => {
            const isActive = this.selectedGenre === genreId ? 'active' : '';
            return `
                <div class="genre-item ${isActive}" data-genre="${genreId}">
                    <div class="genre-item-name">${genreId}</div>
                    <div class="genre-item-category">${this.getCategoryForGenre(genreId)}</div>
                </div>
            `;
        }).join('');
        
        // Add click listeners
        container.querySelectorAll('.genre-item').forEach(item => {
            item.addEventListener('click', () => this.selectGenre(item.dataset.genre));
        });
    }
    
    getCategoryForGenre(genreId) {
        for (const [category, genres] of Object.entries(this.categories)) {
            if (genres.includes(genreId)) {
                return category;
            }
        }
        return 'Unknown';
    }
    
    selectCategory(category) {
        this.currentCategory = category;
        
        // Update active tab
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.category === category) {
                btn.classList.add('active');
            }
        });
        
        // Filter genres
        let filtered = this.genres;
        if (category !== 'all') {
            filtered = this.categories[category] || [];
        }
        
        this.renderGenres(filtered);
    }
    
    async selectGenre(genreId) {
        this.selectedGenre = genreId;
        
        // Update UI
        document.querySelectorAll('.genre-item').forEach(item => {
            item.classList.remove('active');
            if (item.dataset.genre === genreId) {
                item.classList.add('active');
            }
        });
        
        // Load genre info
        await this.loadGenreInfo(genreId);
    }
    
    async loadGenreInfo(genreId) {
        try {
            const response = await fetch(`/api/genre-info?id=${genreId}`);
            const genre = await response.json();
            
            this.displayGenreInfo(genre);
        } catch (error) {
            console.error('Error loading genre info:', error);
        }
    }
    
    displayGenreInfo(genre) {
        const infoContainer = document.getElementById('genreInfo');
        
        infoContainer.innerHTML = `
            <div class="genre-header">
                <h3>${genre.name}</h3>
                <p class="genre-description">${genre.description}</p>
            </div>
        `;
        
        // Update tempo and time signature displays
        document.getElementById('tempoDisplay').textContent = 
            `${genre.tempo_range[0]}-${genre.tempo_range[1]} BPM`;
        
        // Display parameters
        const paramsInfo = document.getElementById('paramsInfo');
        paramsInfo.innerHTML = `
            <div class="param-item">
                <div class="param-label">Swing</div>
                <div class="param-value">${(genre.swing * 100).toFixed(0)}%</div>
            </div>
            <div class="param-item">
                <div class="param-label">Densidad</div>
                <div class="param-value">${(genre.note_density * 100).toFixed(0)}%</div>
            </div>
            <div class="param-item">
                <div class="param-label">Síncopa</div>
                <div class="param-value">${(genre.syncopation * 100).toFixed(0)}%</div>
            </div>
            <div class="param-item">
                <div class="param-label">Complejidad</div>
                <div class="param-value">${(genre.chord_complexity * 100).toFixed(0)}%</div>
            </div>
            <div class="param-item">
                <div class="param-label">Velocidad</div>
                <div class="param-value">${genre.velocity_range[0]}-${genre.velocity_range[1]}</div>
            </div>
            <div class="param-item">
                <div class="param-label">Patrón</div>
                <div class="param-value">${genre.drum_pattern}</div>
            </div>
        `;
        
        // Display instruments
        const instrumentsInfo = document.getElementById('instrumentsInfo');
        instrumentsInfo.innerHTML = genre.instruments
            .map(inst => `<span class="instrument-tag">${inst}</span>`)
            .join('');
    }
    
    async search() {
        const query = document.getElementById('searchInput').value.trim();
        
        if (!query) {
            this.renderGenres(this.genres);
            return;
        }
        
        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();
            this.renderGenres(results);
        } catch (error) {
            console.error('Error searching:', error);
        }
    }
    
    async generate() {
        if (!this.selectedGenre) {
            this.showError('Por favor selecciona un género');
            return;
        }
        
        const bars = parseInt(document.getElementById('barsInput').value);
        const seed = document.getElementById('seedInput').value || null;
        const useNeural = document.getElementById('useNeuralCheckbox').checked;
        
        const generateBtn = document.getElementById('generateBtn');
        const progressContainer = document.getElementById('progressContainer');
        const downloadContainer = document.getElementById('downloadContainer');
        
        // Show progress
        generateBtn.disabled = true;
        progressContainer.style.display = 'block';
        downloadContainer.style.display = 'none';
        
        try {
            const params = new URLSearchParams({
                genre: this.selectedGenre,
                bars: bars,
                neural: useNeural,
                ...(seed && { seed })
            });
            
            const response = await fetch(`/api/generate?${params}`);
            const result = await response.json();
            
            if (result.success) {
                // Show download link
                const downloadLink = document.getElementById('downloadLink');
                downloadLink.href = `/output/${result.filename}`;
                downloadLink.download = result.filename;
                downloadContainer.style.display = 'block';
                
                const neuralNote = useNeural ? ' (con Red Neuronal)' : '';
                this.showSuccess(`✓ MIDI generado: ${result.filename}${neuralNote}`);
            } else {
                this.showError('Error al generar MIDI');
            }
        } catch (error) {
            console.error('Error generating MIDI:', error);
            this.showError('Error al generar MIDI: ' + error.message);
        } finally {
            generateBtn.disabled = false;
            progressContainer.style.display = 'none';
        }
    }
    
    async checkModelStatus() {
        try {
            const response = await fetch('/api/model-status');
            const result = await response.json();
            
            if (result.exists) {
                const statusContainer = document.getElementById('modelStatusContainer');
                const statusText = document.getElementById('modelStatusText');
                statusContainer.style.display = 'block';
                statusText.textContent = `✓ Modelo disponible: ${result.model}`;
                
                // Enable neural checkbox
                document.getElementById('useNeuralCheckbox').disabled = false;
            } else {
                document.getElementById('useNeuralCheckbox').disabled = true;
            }
        } catch (error) {
            console.error('Error checking model status:', error);
            document.getElementById('useNeuralCheckbox').disabled = true;
        }
    }
    
    async trainNeural() {
        const trainingDir = document.getElementById('trainingDirInput').value || 'training_data';
        const epochs = parseInt(document.getElementById('epochsInput').value);
        const modelName = document.getElementById('modelNameInput').value || 'composer_model';
        
        const trainBtn = document.getElementById('trainNeuralBtn');
        const progressContainer = document.getElementById('trainingProgressContainer');
        const statusContainer = document.getElementById('modelStatusContainer');
        
        // Validate
        if (!trainingDir) {
            this.showError('Por favor especifica un directorio de entrenamiento');
            return;
        }
        
        // Show progress
        trainBtn.disabled = true;
        progressContainer.style.display = 'block';
        statusContainer.style.display = 'none';
        
        try {
            const response = await fetch('/api/train-neural', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    directory: trainingDir,
                    epochs: epochs,
                    model_name: modelName
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showSuccess(`✓ Modelo entrenado: ${result.model}`);
                
                // Update status
                const statusText = document.getElementById('modelStatusText');
                statusText.textContent = `✓ Modelo disponible: ${result.model}`;
                statusContainer.style.display = 'block';
                
                // Enable neural checkbox
                document.getElementById('useNeuralCheckbox').disabled = false;
                document.getElementById('useNeuralCheckbox').checked = true;
            } else {
                const errorMsg = result.error || 'Error al entrenar el modelo';
                this.showError(errorMsg);
            }
        } catch (error) {
            console.error('Error training neural model:', error);
            this.showError('Error al entrenar: ' + error.message);
        } finally {
            trainBtn.disabled = false;
            progressContainer.style.display = 'none';
        }
    }
    
    showError(message) {
        alert('❌ ' + message);
    }
    
    showSuccess(message) {
        alert(message);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ComposerApp();
});
