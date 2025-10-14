#!/bin/bash

# BatmanWL Bot Startup Script

echo "🦇 Iniciando BatmanWL Bot..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado"
    echo "Por favor, ejecuta ./install.sh primero"
    exit 1
fi

# Check if config exists
if [ ! -f "config.ini" ]; then
    echo "❌ config.ini no encontrado"
    echo "Por favor, crea el archivo de configuración"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start bot
python bot.py
