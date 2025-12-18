# Frontend Guide - Universal Genre MIDI Composer

## Descripción General

El frontend es una **interfaz web moderna y responsiva** que permite generar música MIDI en 200+ géneros musicales sin necesidad de línea de comandos.

## Arquitectura

```
Frontend (HTML/CSS/JavaScript)
    ↓
Web Server (Python)
    ↓
Compositor Universal
    ↓
Generador MIDI
    ↓
Archivo .mid
```

## Componentes

### 1. **index.html** - Estructura
- Header con título y descripción
- Panel izquierdo: Selección de géneros
- Panel derecho: Configuración y generación
- Footer con información

### 2. **style.css** - Estilos
- Diseño moderno con gradientes
- Tema oscuro profesional
- Responsive para móvil/tablet/desktop
- Animaciones suaves
- Colores: Indigo, Púrpura, Rosa

### 3. **app.js** - Lógica
- Carga de géneros desde API
- Búsqueda y filtrado
- Selección de categorías
- Generación de MIDI
- Descarga de archivos

### 4. **web_server.py** - Backend
- Servidor HTTP en Python
- API REST para géneros
- Generación de MIDI
- Servicio de archivos estáticos

## Interfaz de Usuario

### Panel Izquierdo: Selección de Géneros

```
┌─────────────────────────────┐
│ Selecciona un Género        │
├─────────────────────────────┤
│ [Buscar...]          [🔍]   │
├─────────────────────────────┤
│ [Todos] [Rock] [Metal] ...  │
├─────────────────────────────┤
│ • trap                      │
│ • jazz_fusion               │
│ • salsa                     │
│ • soviet_rock               │
│ ...                         │
└─────────────────────────────┘
```

**Características:**
- Búsqueda en tiempo real
- Filtrado por categoría
- Selección con click
- Indicador de género activo

### Panel Derecho: Configuración

```
┌─────────────────────────────┐
│ Información del Género      │
│ Trap                        │
│ Música electrónica urbana   │
├─────────────────────────────┤
│ Configuración               │
│ Compases: [32]              │
│ Seed: [________]  [🎲]      │
│ Tempo: 130-170 BPM          │
│ Compás: 4/4                 │
│                             │
│ [▶ Generar MIDI]            │
│                             │
│ [⬇ Descargar MIDI]          │
├─────────────────────────────┤
│ Parámetros | Instrumentos   │
│ Swing: 0%                   │
│ Densidad: 60%               │
│ ...                         │
└─────────────────────────────┘
```

**Características:**
- Información del género
- Controles de configuración
- Botón de generación
- Descarga de archivos
- Parámetros técnicos

## Flujo de Uso

### 1. Carga Inicial
```
Usuario abre index.html
    ↓
JavaScript carga app.js
    ↓
app.js solicita /api/genres
    ↓
web_server.py devuelve lista de géneros
    ↓
Interfaz muestra géneros
```

### 2. Selección de Género
```
Usuario hace click en género
    ↓
app.js solicita /api/genre-info?id=trap
    ↓
web_server.py devuelve parámetros
    ↓
Interfaz muestra información
```

### 3. Generación de MIDI
```
Usuario hace click en "Generar MIDI"
    ↓
app.js solicita /api/generate?genre=trap&bars=32
    ↓
web_server.py:
  - Crea GenreComposer
  - Genera melodía, acordes, bajo, batería
  - Crea archivo MIDI
  - Guarda en output/
    ↓
app.js recibe nombre de archivo
    ↓
Interfaz muestra botón de descarga
    ↓
Usuario descarga archivo
```

## API REST

### Endpoints

#### GET /api/genres
Devuelve lista de todos los géneros
```json
["trap", "jazz_fusion", "salsa", ...]
```

#### GET /api/categories
Devuelve géneros organizados por categoría
```json
{
  "Rock": ["punk_rock", "grunge", ...],
  "Metal": ["death_metal", "symphonic_metal", ...],
  ...
}
```

#### GET /api/genre-info?id=trap
Devuelve información detallada de un género
```json
{
  "id": "trap",
  "name": "Trap",
  "category": "Hip-Hop",
  "description": "...",
  "tempo_range": [130, 170],
  "scales": ["minor", "phrygian"],
  "swing": 0.0,
  "velocity_range": [80, 120],
  "note_density": 0.6,
  "syncopation": 0.6,
  "instruments": ["808", "hi_hats", "synth"],
  "drum_pattern": "trap",
  "bass_style": "808_bass",
  "chord_complexity": 0.2
}
```

#### GET /api/search?q=metal
Busca géneros por palabra clave
```json
["heavy_metal", "death_metal", "black_metal", ...]
```

#### GET /api/generate?genre=trap&bars=32&seed=42
Genera archivo MIDI
```json
{
  "success": true,
  "filename": "trap_32bars.mid"
}
```

## Estructura de Archivos

```
a_dawn_composer/
├── index.html          # Página principal
├── style.css           # Estilos
├── app.js              # Lógica del frontend
├── web_server.py       # Servidor web
├── run.bat             # Launcher Windows
├── run.sh              # Launcher Linux/macOS
├── output/             # Archivos MIDI generados
│   ├── trap_32bars.mid
│   ├── jazz_fusion_64bars.mid
│   └── ...
└── genres/             # Base de datos de géneros
    └── ...
```

## Personalización

### Cambiar Puerto
Edita `web_server.py`:
```python
start_server(8000)  # Cambiar a 8001, 8080, etc.
```

### Cambiar Colores
Edita `style.css`:
```css
:root {
    --primary-color: #6366f1;      /* Indigo */
    --secondary-color: #8b5cf6;    /* Púrpura */
    --accent-color: #ec4899;       /* Rosa */
    ...
}
```

### Agregar Géneros
Edita archivos en `genres/`:
```python
TRAP_GENRES = {
    "trap": GenreParams(
        name="Trap",
        category="Hip-Hop",
        ...
    )
}
```

## Características Avanzadas

### Búsqueda en Tiempo Real
- Busca mientras escribes
- Filtra por nombre, categoría, descripción
- Resultados instantáneos

### Categorías Dinámicas
- Pestañas para cada categoría
- Filtrado automático
- Actualización en tiempo real

### Información Detallada
- Parámetros técnicos
- Instrumentos típicos
- Rango de tempo
- Complejidad armónica

### Reproducibilidad
- Campo de seed para reproducir composiciones
- Botón aleatorio para generar seed
- Mismo seed = misma música

## Rendimiento

- **Carga inicial**: < 1 segundo
- **Búsqueda**: < 100ms
- **Generación MIDI**: 1-3 segundos
- **Descarga**: Instantánea

## Compatibilidad

### Navegadores
- Chrome/Chromium ✓
- Firefox ✓
- Safari ✓
- Edge ✓

### Sistemas Operativos
- Windows ✓
- macOS ✓
- Linux ✓

### DAWs Compatibles
- Ableton Live ✓
- FL Studio ✓
- Logic Pro ✓
- GarageBand ✓
- Reaper ✓
- Cubase ✓
- Studio One ✓
- Cualquier DAW que soporte MIDI ✓

## Seguridad

- No se almacenan datos personales
- Los archivos se generan localmente
- No hay conexión a internet requerida
- Servidor local (localhost)

## Próximas Mejoras

- [ ] Historial de generaciones
- [ ] Presets personalizados
- [ ] Exportar a otros formatos (WAV, MP3)
- [ ] Visualizador de notas
- [ ] Editor de parámetros en tiempo real
- [ ] Grabación de audio en vivo
- [ ] Compartir composiciones

## Troubleshooting

### El servidor no inicia
```bash
# Verifica que el puerto esté disponible
netstat -an | grep 8000

# O usa otro puerto
python web_server.py 8001
```

### Los géneros no cargan
```bash
# Verifica que los archivos de géneros existan
ls genres/

# Verifica que Python pueda importarlos
python -c "from genres.all_genres import get_genre_count; print(get_genre_count())"
```

### El MIDI no se genera
```bash
# Verifica que midiutil esté instalado
python -m pip install midiutil

# Verifica que la carpeta output exista
mkdir output
```

## Documentación Relacionada

- `README.md` - Guía general
- `SETUP_GUIDE.md` - Instalación
- `QUICK_START.md` - Inicio rápido
- `GENRES_LIST.md` - Lista de géneros
- `DOCUMENTATION.md` - Documentación técnica

¡Disfruta creando música! 🎵
