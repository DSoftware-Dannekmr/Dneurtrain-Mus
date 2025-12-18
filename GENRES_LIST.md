# Complete Musical Genres Database

This composer supports **200+ musical genres and subgenres** organized into categories.

## Categories

### Rock (20 genres)
- rock_and_roll, hard_rock, punk_rock, grunge, indie_rock
- progressive_rock, glam_rock, alternative_rock, psychedelic_rock
- garage_rock, post_rock, shoegaze, britpop, emo, post_grunge
- stoner_rock, southern_rock, art_rock, surf_rock, blues_rock

### Metal (19 genres)
- heavy_metal, thrash_metal, death_metal, black_metal, doom_metal
- power_metal, symphonic_metal, progressive_metal, nu_metal
- groove_metal, melodic_death_metal, folk_metal, industrial_metal
- sludge_metal, djent, gothic_metal, speed_metal, crossover_thrash

### Electronic (40+ genres)
**House:** house, deep_house, tech_house, progressive_house, electro_house, acid_house
**Techno:** techno, detroit_techno, minimal_techno, dub_techno
**Trance:** trance, progressive_trance, psytrance, goa_trance
**DnB:** drum_and_bass, liquid_dnb, neurofunk, jungle
**Dubstep:** dubstep, brostep
**Ambient:** ambient, dark_ambient, chillout, downtempo, trip_hop
**Other:** synthwave, vaporwave, idm, breakbeat, hardcore_techno, gabber, future_bass, tropical_house, moombahton, chillwave, witch_house

### Jazz (15 genres)
- bebop, cool_jazz, free_jazz, jazz_fusion, smooth_jazz
- acid_jazz, swing, dixieland, latin_jazz, modal_jazz
- hard_bop, post_bop, gypsy_jazz, nu_jazz, ethno_jazz

### Blues (8 genres)
- delta_blues, chicago_blues, electric_blues, country_blues
- jump_blues, texas_blues, piedmont_blues, west_coast_blues

### Pop (13 genres)
- pop, synthpop, electropop, dance_pop, teen_pop
- indie_pop, dream_pop, kpop, jpop, latin_pop
- bedroom_pop, hyperpop

### R&B / Soul / Funk (15 genres)
**R&B:** rnb, contemporary_rnb, new_jack_swing, alternative_rnb
**Soul:** soul, motown, neo_soul, southern_soul, psychedelic_soul
**Funk:** funk, p_funk, funk_rock, electro_funk, boogie

### Hip-Hop (16 genres)
- hip_hop, old_school_hip_hop, boom_bap, gangsta_rap, trap
- drill, conscious_rap, jazz_rap, lofi_hip_hop, horrorcore
- crunk, cloud_rap, phonk, uk_grime, afrotrap, latin_trap

### Latin (22 genres)
- salsa, bachata, merengue, cumbia, reggaeton, bolero
- son_cubano, tango, nortena, banda, corrido, ranchera
- mariachi, bossa_nova, samba, forró, baile_funk
- vallenato, champeta, electrocumbia

### World Music (30+ genres)
**African:** afrobeat, afropop, highlife, soukous, kizomba, amapiano, gqom, mbalax, afroswing
**Middle Eastern:** arabic_classical, shaabi, mahraganat, raqs_sharqi
**Indian:** hindustani_classical, carnatic, bollywood, bhangra
**European:** flamenco, fado, celtic, balkan, klezmer, polka
**Asian:** japanese_traditional, enka, chinese_traditional, cantopop
**Caribbean:** reggae, dub, dancehall, calypso, soca

### Classical / Cinematic (15 genres)
**Classical:** baroque, classical_period, romantic, impressionist, modernist, minimalist, neoclassical, contemporary_classical
**Cinematic:** film_score, epic_orchestral, trailer_music, ambient_score, videogame_music
**New Age:** new_age, meditation_music, space_music

### Country / Folk / Gospel (20 genres)
**Country:** country, bluegrass, honky_tonk, outlaw_country, country_pop, country_rock, americana, alt_country, western_swing
**Folk:** folk, folk_rock, indie_folk, chamber_folk, neofolk, appalachian, old_time
**Gospel:** gospel, southern_gospel, contemporary_christian, urban_gospel, spirituals

### Punk / Ska / Industrial (20 genres)
**Punk:** punk, hardcore_punk, post_punk, pop_punk, skate_punk, oi, anarcho_punk, crust_punk, garage_punk
**Ska:** ska, two_tone, ska_punk, rocksteady
**Industrial:** industrial, industrial_rock, darkwave, ebm, aggrotech, power_noise

### Experimental / Digital (15 genres)
**Experimental:** noise, drone, musique_concrete, free_improvisation, electroacoustic, avant_prog, glitch, plunderphonics, sound_art
**Digital:** chiptune, bitpop, algorave, generative_music, ai_generated, future_funk, chillhop, vaportrap

### Russian / Soviet (3 genres)
- soviet_rock (Kino/Viktor Tsoy style)
- russian_post_punk
- russian_chanson

## Usage

```bash
# Generate MIDI in any genre
python generate_any_genre.py trap
python generate_any_genre.py jazz_fusion -b 64
python generate_any_genre.py salsa -o my_salsa.mid

# List all genres
python generate_any_genre.py --list

# Search genres
python generate_any_genre.py --search metal

# Get genre info
python generate_any_genre.py --info bebop
```

## Genre Parameters

Each genre includes:
- **Tempo range** (BPM min-max)
- **Time signatures** (4/4, 3/4, 6/8, 7/8, etc.)
- **Scales** (major, minor, modes, ethnic scales)
- **Swing amount** (0.0 = straight, 1.0 = full swing)
- **Velocity range** (dynamics)
- **Note density** (sparse to dense)
- **Syncopation level**
- **Typical instruments**
- **Drum pattern type**
- **Bass style**
- **Chord complexity**
