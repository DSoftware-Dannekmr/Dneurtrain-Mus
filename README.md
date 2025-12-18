# Universal Genre-Based MIDI Composer

Un compositor de música MIDI completamente parametrizado que puede generar composiciones en **200+ géneros musicales** diferentes.

## Instalación

### 1. Instalar Python
Si no tienes Python instalado, descárgalo desde: https://www.python.org/downloads/

Durante la instalación, **marca la opción "Add Python to PATH"**.

### 2. Instalar dependencias

```bash
pip install midiutil numpy mido
```

Opcional (para características de red neuronal):
```bash
pip install tensorflow
```

### 3. Ejecutar la plataforma

**Windows:**
```bash
run.bat
```

**Linux/macOS:**
```bash
bash run.sh
```

O manualmente:
```bash
python web_server.py
```

Luego abre http://localhost:8000 en tu navegador.

## Uso

### Generar MIDI en cualquier género

```bash
# Generar en género Trap
python generate_any_genre.py trap

# Generar en Jazz Fusion con 64 compases
python generate_any_genre.py jazz_fusion -b 64

# Generar Salsa y guardar como archivo específico
python generate_any_genre.py salsa -o mi_salsa.mid

# Generar con seed específico (reproducible)
python generate_any_genre.py soviet_rock -s 42
```

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

## Géneros Disponibles

### Rock (20 géneros)
rock_and_roll, hard_rock, punk_rock, grunge, indie_rock, progressive_rock, glam_rock, alternative_rock, psychedelic_rock, garage_rock, post_rock, shoegaze, britpop, emo, post_grunge, stoner_rock, southern_rock, art_rock, surf_rock, blues_rock

### Metal (19 géneros)
heavy_metal, thrash_metal, death_metal, black_metal, doom_metal, power_metal, symphonic_metal, progressive_metal, nu_metal, groove_metal, melodic_death_metal, folk_metal, industrial_metal, sludge_metal, djent, gothic_metal, speed_metal, crossover_thrash

### Electrónica (40+ géneros)
house, deep_house, tech_house, progressive_house, electro_house, acid_house, techno, detroit_techno, minimal_techno, dub_techno, trance, progressive_trance, psytrance, goa_trance, drum_and_bass, liquid_dnb, neurofunk, jungle, dubstep, brostep, ambient, dark_ambient, chillout, downtempo, trip_hop, synthwave, vaporwave, idm, breakbeat, hardcore_techno, gabber, future_bass, tropical_house, moombahton, chillwave, witch_house

### Jazz (15 géneros)
bebop, cool_jazz, free_jazz, jazz_fusion, smooth_jazz, acid_jazz, swing, dixieland, latin_jazz, modal_jazz, hard_bop, post_bop, gypsy_jazz, nu_jazz, ethno_jazz

### Blues (8 géneros)
delta_blues, chicago_blues, electric_blues, country_blues, jump_blues, texas_blues, piedmont_blues, west_coast_blues

### Pop (13 géneros)
pop, synthpop, electropop, dance_pop, teen_pop, indie_pop, dream_pop, kpop, jpop, latin_pop, bedroom_pop, hyperpop

### R&B / Soul / Funk (15 géneros)
rnb, contemporary_rnb, new_jack_swing, alternative_rnb, soul, motown, neo_soul, southern_soul, psychedelic_soul, funk, p_funk, funk_rock, electro_funk, boogie

### Hip-Hop (16 géneros)
hip_hop, old_school_hip_hop, boom_bap, gangsta_rap, trap, drill, conscious_rap, jazz_rap, lofi_hip_hop, horrorcore, crunk, cloud_rap, phonk, uk_grime, afrotrap, latin_trap

### Latina (22 géneros)
salsa, bachata, merengue, cumbia, reggaeton, bolero, son_cubano, tango, nortena, banda, corrido, ranchera, mariachi, bossa_nova, samba, forró, baile_funk, vallenato, champeta, electrocumbia

### Música del Mundo (30+ géneros)
**Africana:** afrobeat, afropop, highlife, soukous, kizomba, amapiano, gqom, mbalax, afroswing
**Árabe:** arabic_classical, shaabi, mahraganat, raqs_sharqi
**India:** hindustani_classical, carnatic, bollywood, bhangra
**Europea:** flamenco, fado, celtic, balkan, klezmer, polka
**Asiática:** japanese_traditional, enka, chinese_traditional, cantopop
**Caribeña:** reggae, dub, dancehall, calypso, soca

### Clásica / Cinematográfica (15 géneros)
baroque, classical_period, romantic, impressionist, modernist, minimalist, neoclassical, contemporary_classical, film_score, epic_orchestral, trailer_music, ambient_score, videogame_music, new_age, meditation_music, space_music

### Country / Folk / Gospel (20 géneros)
country, bluegrass, honky_tonk, outlaw_country, country_pop, country_rock, americana, alt_country, western_swing, folk, folk_rock, indie_folk, chamber_folk, neofolk, appalachian, old_time, gospel, southern_gospel, contemporary_christian, urban_gospel, spirituals

### Punk / Ska / Industrial (20 géneros)
punk, hardcore_punk, post_punk, pop_punk, skate_punk, oi, anarcho_punk, crust_punk, garage_punk, ska, two_tone, ska_punk, rocksteady, industrial, industrial_rock, darkwave, ebm, aggrotech, power_noise

### Experimental / Digital (15 géneros)
noise, drone, musique_concrete, free_improvisation, electroacoustic, avant_prog, glitch, plunderphonics, sound_art, chiptune, bitpop, algorave, generative_music, ai_generated, future_funk, chillhop, vaportrap

### Ruso / Soviético (3 géneros)
soviet_rock, russian_post_punk, russian_chanson

## Estructura de Archivos

```
a_dawn_composer/
├── genres/
│   ├── genre_database.py       # Base de datos de parámetros
│   ├── rock_genres.py          # Géneros de rock
│   ├── metal_genres.py         # Géneros de metal
│   ├── electronic_genres.py    # Géneros electrónicos
│   ├── jazz_blues_genres.py    # Jazz y Blues
│   ├── pop_rnb_genres.py       # Pop, R&B, Soul, Funk
│   ├── hiphop_genres.py        # Hip-Hop
│   ├── latin_genres.py         # Música Latina
│   ├── world_genres.py         # Música del Mundo
│   ├── classical_genres.py     # Clásica y Cinematográfica
│   ├── country_folk_genres.py  # Country, Folk, Gospel
│   ├── punk_ska_genres.py      # Punk, Ska, Industrial
│   ├── experimental_genres.py  # Experimental, Digital, Soviet
│   └── all_genres.py           # Registro maestro
├── universal_composer.py       # Motor de composición
├── generate_any_genre.py       # Script principal
└── README.md                   # Este archivo
```

## Parámetros de Género

Cada género incluye:
- **Tempo**: Rango de BPM
- **Time Signatures**: Compases soportados
- **Escalas**: Escalas musicales usadas
- **Swing**: Cantidad de swing (0.0 = recto, 1.0 = full swing)
- **Velocity Range**: Rango dinámico
- **Note Density**: Densidad de notas (0.0 = sparse, 1.0 = dense)
- **Syncopation**: Nivel de síncopa
- **Instruments**: Instrumentos típicos
- **Drum Pattern**: Tipo de patrón de batería
- **Bass Style**: Estilo de línea de bajo
- **Chord Complexity**: Complejidad armónica

## Ejemplos de Uso

### Generar una canción de Trap
```bash
python generate_any_genre.py trap -b 32 -o trap_beat.mid
```

### Generar Jazz Fusion
```bash
python generate_any_genre.py jazz_fusion -b 64
```

### Generar Salsa
```bash
python generate_any_genre.py salsa -b 48
```

### Generar Música Clásica Minimalista
```bash
python generate_any_genre.py minimalist -b 128
```

### Generar Música Soviética (Kino style)
```bash
python generate_any_genre.py soviet_rock -b 32
```

## Características

✓ 200+ géneros musicales
✓ Parámetros específicos por género
✓ Generación de 4 pistas: Melodía, Acordes, Bajo, Batería
✓ Patrones de batería específicos por género
✓ Líneas de bajo adaptadas al género
✓ Escalas y modos musicales auténticos
✓ Reproducible con seeds
✓ Exporta a MIDI estándar
✓ **Red Neuronal LSTM con Atención** para mejorar composiciones
✓ Entrenamiento en archivos MIDI externos
✓ Interfaz web moderna e intuitiva
✓ Generación con mejora neuronal opcional

## Red Neuronal (NEW!)

### Entrenar un Modelo

1. **Preparar datos**: Coloca archivos MIDI en la carpeta `training_data/`
2. **Entrenar**: 
   - Vía web: Usa la sección "🧠 Red Neuronal" en la interfaz
   - Vía CLI: `python train_neural.py -e 100`
3. **Usar**: Marca "Usar Red Neuronal" al generar MIDI

### Características de la Red Neuronal

- **LSTM Bidireccional**: Aprende patrones en ambas direcciones
- **Mecanismo de Atención**: Identifica partes importantes de la secuencia
- **Entrenamiento Flexible**: Entrena en tus propios archivos MIDI
- **Mejora Seamless**: Se integra perfectamente con la composición algorítmica
- **Modelos Persistentes**: Guarda y reutiliza modelos entrenados

### Ejemplo: Entrenar y Generar

```bash
# 1. Entrenar modelo
python train_neural.py -d training_data -e 100 -m mi_modelo

# 2. Generar con mejora neuronal
# Usa la interfaz web o:
from advanced_neural_network import AdvancedNeuralComposer
from universal_composer import GenreComposer

neural_model = AdvancedNeuralComposer()
neural_model.load_model('models/mi_modelo.h5')

composer = GenreComposer('jazz_fusion', neural_model=neural_model)
melody = composer.generate_melody(bars=32)
```

Para más detalles, ver `NEURAL_NETWORK_GUIDE.md`

## Notas Técnicas

- Los archivos MIDI generados tienen 4 pistas:
  1. **Melody**: Línea melódica principal
  2. **Chords**: Progresión armónica
  3. **Bass**: Línea de bajo
  4. **Drums**: Patrón de batería

- Cada pista puede usarse independientemente como loop
- Compatible con cualquier DAW (Ableton, FL Studio, Logic, etc.)
- Formato MIDI estándar (Type 1)
- Los archivos generados con red neuronal tienen sufijo `_neural`

## Solución de Problemas

### "Python no se encuentra"
- Reinstala Python desde https://www.python.org/downloads/
- Marca "Add Python to PATH" durante la instalación

### "midiutil no encontrado"
```bash
pip install midiutil
```

### "No se puede generar MIDI"
Verifica que tengas permisos de escritura en la carpeta actual.

## Licencia

Libre para uso educativo y personal.

## Autor

Compositor Neural Global - GEMINI KIRO
