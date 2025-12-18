# Quick Start - Universal Genre MIDI Composer

## Inicio Rápido

### Windows

1. **Abre el archivo `run.bat`** haciendo doble clic
2. El navegador se abrirá automáticamente en `http://localhost:8000`
3. ¡Comienza a generar música!

### macOS / Linux

1. **Abre una terminal** en la carpeta `a_dawn_composer`
2. **Ejecuta el script:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
3. El navegador se abrirá automáticamente en `http://localhost:8000`
4. ¡Comienza a generar música!

## Uso de la Interfaz Web

### 1. Selecciona un Género
- Usa la **barra de búsqueda** para encontrar géneros
- O haz clic en las **pestañas de categoría** (Rock, Metal, Electrónica, etc.)
- Haz clic en un género para seleccionarlo

### 2. Configura los Parámetros
- **Compases**: Número de compases a generar (4-256)
- **Seed**: Número para reproducibilidad (opcional)
- Los parámetros del género se muestran automáticamente

### 3. Genera el MIDI
- Haz clic en el botón **"▶ Generar MIDI"**
- Espera a que se complete la generación
- Haz clic en **"⬇ Descargar MIDI"** para descargar el archivo

### 4. Abre en tu DAW
- Abre el archivo MIDI en tu DAW favorito:
  - Ableton Live
  - FL Studio
  - Logic Pro
  - GarageBand
  - Reaper
  - Cualquier otro DAW

## Ejemplos de Géneros

### Rock
- `punk_rock` - Punk rápido y agresivo
- `progressive_rock` - Rock progresivo complejo
- `grunge` - Grunge oscuro y pesado

### Metal
- `death_metal` - Metal extremo
- `symphonic_metal` - Metal sinfónico
- `djent` - Djent polirrítmico

### Electrónica
- `trap` - Trap moderno
- `psytrance` - Psytrance hipnótico
- `ambient` - Ambient atmosférico

### Jazz
- `bebop` - Bebop clásico
- `jazz_fusion` - Jazz fusion
- `smooth_jazz` - Smooth jazz

### Latina
- `salsa` - Salsa cubana
- `reggaeton` - Reggaetón urbano
- `bossa_nova` - Bossa nova brasileña

### Clásica
- `minimalist` - Minimalismo
- `baroque` - Barroco
- `film_score` - Música de cine

## Solución de Problemas

### "Python no se encuentra"
- **Windows**: Reinstala Python desde https://www.python.org/downloads/
  - Marca "Add Python to PATH" durante la instalación
- **macOS**: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

### "midiutil no encontrado"
```bash
python -m pip install midiutil numpy
```

### El navegador no se abre automáticamente
- Abre manualmente: http://localhost:8000

### "Puerto 8000 ya está en uso"
- Edita `web_server.py` y cambia el puerto en la última línea
- O ejecuta: `python web_server.py 8001`

## Características

✓ 200+ géneros musicales
✓ Interfaz web intuitiva
✓ Generación en tiempo real
✓ 4 pistas MIDI (Melodía, Acordes, Bajo, Batería)
✓ Parámetros específicos por género
✓ Descarga directa de archivos MIDI
✓ Compatible con cualquier DAW

## Archivos Generados

Los archivos MIDI se guardan en la carpeta `output/`:
- `trap_32bars.mid`
- `jazz_fusion_64bars.mid`
- `salsa_48bars.mid`
- etc.

## Próximos Pasos

1. Genera varios MIDIs en diferentes géneros
2. Abre los archivos en tu DAW favorito
3. Edita, mezcla y personaliza
4. Experimenta con diferentes parámetros
5. ¡Crea tu propia música!

## Soporte

Si tienes problemas:
1. Verifica que Python esté instalado: `python --version`
2. Verifica que midiutil esté instalado: `python -m pip install midiutil`
3. Intenta ejecutar desde una terminal nueva
4. Revisa los logs en la terminal

## Más Información

- Ver lista completa de géneros: `GENRES_LIST.md`
- Documentación técnica: `DOCUMENTATION.md`
- Guía de configuración: `SETUP_GUIDE.md`

¡Diviértete creando música! 🎵
