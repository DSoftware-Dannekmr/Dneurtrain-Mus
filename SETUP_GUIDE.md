# Guía de Configuración - Compositor Neural Global

## Paso 1: Instalar Python

### Windows
1. Ve a https://www.python.org/downloads/
2. Descarga Python 3.11 o superior
3. Ejecuta el instalador
4. **IMPORTANTE**: Marca la casilla "Add Python to PATH"
5. Haz clic en "Install Now"

### macOS
```bash
# Con Homebrew
brew install python3

# O descarga desde https://www.python.org/downloads/
```

### Linux
```bash
sudo apt-get install python3 python3-pip
```

## Paso 2: Instalar Dependencias

Abre una terminal/cmd en la carpeta `a_dawn_composer` y ejecuta:

```bash
pip install midiutil numpy
```

Opcional (para características avanzadas):
```bash
pip install tensorflow
```

## Paso 3: Verificar Instalación

```bash
python test_genres.py
```

Deberías ver algo como:
```
✓ Genres module loaded successfully

Total genres: 200+
Total categories: 20+

Genres by category:
  Rock: 20 genres
  Metal: 19 genres
  Electronic: 40+ genres
  ...

✓ All tests passed!
```

## Paso 4: Generar tu Primer MIDI

```bash
# Generar Trap
python generate_any_genre.py trap

# Generar Jazz Fusion
python generate_any_genre.py jazz_fusion -b 64

# Generar Salsa
python generate_any_genre.py salsa -o mi_salsa.mid
```

## Comandos Útiles

### Listar todos los géneros
```bash
python generate_any_genre.py --list
```

### Buscar géneros
```bash
python generate_any_genre.py --search metal
python generate_any_genre.py --search latin
python generate_any_genre.py --search electronic
```

### Ver información de un género
```bash
python generate_any_genre.py --info bebop
python generate_any_genre.py --info trap
python generate_any_genre.py --info flamenco
```

### Generar con opciones
```bash
# Especificar número de compases
python generate_any_genre.py trap -b 64

# Especificar archivo de salida
python generate_any_genre.py salsa -o mi_salsa.mid

# Usar seed para reproducibilidad
python generate_any_genre.py jazz_fusion -s 42

# Combinar opciones
python generate_any_genre.py soviet_rock -b 32 -o kino.mid -s 123
```

## Solución de Problemas

### Error: "python: command not found"
**Solución**: Python no está en PATH. Reinstala Python y marca "Add Python to PATH".

### Error: "No module named 'midiutil'"
**Solución**: Instala las dependencias:
```bash
pip install midiutil numpy
```

### Error: "TS_11_8 not found"
**Solución**: Ya está corregido en la versión actual. Actualiza los archivos.

### Error: "Permission denied"
**Solución**: Verifica que tengas permisos de escritura en la carpeta.

## Archivos Generados

Cuando ejecutas `python generate_any_genre.py trap`, se crea:
- `trap.mid` - Archivo MIDI con 4 pistas

Puedes abrir este archivo en:
- **Ableton Live**
- **FL Studio**
- **Logic Pro**
- **GarageBand**
- **Reaper**
- **Cualquier DAW**

## Estructura del Proyecto

```
a_dawn_composer/
├── genres/                      # Base de datos de géneros
│   ├── genre_database.py        # Definiciones base
│   ├── rock_genres.py           # 20 géneros de rock
│   ├── metal_genres.py          # 19 géneros de metal
│   ├── electronic_genres.py     # 40+ géneros electrónicos
│   ├── jazz_blues_genres.py     # Jazz y Blues
│   ├── pop_rnb_genres.py        # Pop, R&B, Soul, Funk
│   ├── hiphop_genres.py         # Hip-Hop
│   ├── latin_genres.py          # Música Latina
│   ├── world_genres.py          # Música del Mundo
│   ├── classical_genres.py      # Clásica y Cinematográfica
│   ├── country_folk_genres.py   # Country, Folk, Gospel
│   ├── punk_ska_genres.py       # Punk, Ska, Industrial
│   ├── experimental_genres.py   # Experimental, Digital, Soviet
│   └── all_genres.py            # Registro maestro
├── universal_composer.py        # Motor de composición
├── generate_any_genre.py        # Script principal
├── test_genres.py               # Script de prueba
├── README.md                    # Documentación
├── SETUP_GUIDE.md              # Esta guía
└── GENRES_LIST.md              # Lista de géneros
```

## Ejemplos de Géneros

### Rock
```bash
python generate_any_genre.py punk_rock
python generate_any_genre.py progressive_rock -b 128
python generate_any_genre.py grunge
```

### Metal
```bash
python generate_any_genre.py death_metal
python generate_any_genre.py symphonic_metal -b 64
python generate_any_genre.py djent
```

### Electrónica
```bash
python generate_any_genre.py house
python generate_any_genre.py psytrance -b 64
python generate_any_genre.py ambient -b 256
```

### Jazz
```bash
python generate_any_genre.py bebop
python generate_any_genre.py jazz_fusion -b 64
python generate_any_genre.py smooth_jazz
```

### Latina
```bash
python generate_any_genre.py salsa -b 48
python generate_any_genre.py reggaeton
python generate_any_genre.py bossa_nova
```

### Clásica
```bash
python generate_any_genre.py minimalist -b 128
python generate_any_genre.py baroque
python generate_any_genre.py film_score -b 64
```

### Experimental
```bash
python generate_any_genre.py ambient
python generate_any_genre.py glitch
python generate_any_genre.py chiptune
```

## Características Principales

✓ **200+ géneros musicales** - Todos los géneros principales y subgéneros
✓ **Parámetros específicos** - Cada género tiene tempo, escalas, patrones únicos
✓ **4 pistas MIDI** - Melodía, Acordes, Bajo, Batería
✓ **Patrones auténticos** - Drum patterns, bass lines, chord progressions específicas
✓ **Escalas reales** - Modos, escalas étnicas, pentatónicas, etc.
✓ **Reproducible** - Usa seeds para generar la misma música
✓ **Exporta MIDI** - Compatible con cualquier DAW

## Próximos Pasos

1. Genera algunos MIDIs en diferentes géneros
2. Abre los archivos en tu DAW favorito
3. Edita, mezcla y personaliza
4. Experimenta con diferentes géneros y parámetros

¡Diviértete creando música!
