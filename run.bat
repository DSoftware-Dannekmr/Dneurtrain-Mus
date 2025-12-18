@echo off
REM Universal Genre MIDI Composer - Windows Launcher
REM Este script inicia el servidor web y abre el navegador

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Universal Genre MIDI Composer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH
    echo.
    echo Por favor:
    echo 1. Descarga Python desde https://www.python.org/downloads/
    echo 2. Durante la instalacion, marca "Add Python to PATH"
    echo 3. Reinicia este script
    echo.
    pause
    exit /b 1
)

REM Check if midiutil is installed
python -c "import midiutil" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    python -m pip install midiutil numpy
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

REM Create output directory
if not exist "output" mkdir output

REM Start the server
echo Iniciando servidor...
echo.
echo Abriendo navegador en http://localhost:8000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python web_server.py

pause
