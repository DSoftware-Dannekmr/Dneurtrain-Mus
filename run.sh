#!/bin/bash
# Universal Genre MIDI Composer - Linux/macOS Launcher

echo ""
echo "========================================"
echo "Universal Genre MIDI Composer"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no esta instalado"
    echo ""
    echo "Por favor instala Python 3:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt-get install python3 python3-pip"
    echo ""
    exit 1
fi

# Check if midiutil is installed
python3 -c "import midiutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependencias..."
    python3 -m pip install midiutil numpy
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudieron instalar las dependencias"
        exit 1
    fi
fi

# Create output directory
mkdir -p output

# Start the server
echo "Iniciando servidor..."
echo ""
echo "Abriendo navegador en http://localhost:8000"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

python3 web_server.py
