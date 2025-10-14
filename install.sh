#!/bin/bash

# BatmanWL Bot Installer
# Simplified deployment script

echo "🦇 BatmanWL Bot - Instalador 🦇"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "Por favor, instala Python 3.8 o superior"
    exit 1
fi

echo "✅ Python 3 detectado: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    echo "Por favor, instala pip3"
    exit 1
fi

echo "✅ pip3 detectado"
echo ""

# Create virtual environment
echo "📦 Creando entorno virtual..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Error al crear entorno virtual"
    exit 1
fi

echo "✅ Entorno virtual creado"
echo ""

# Activate virtual environment
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

echo "✅ Dependencias instaladas"
echo ""

# Create config file if it doesn't exist
if [ ! -f config.ini ]; then
    echo "⚙️  Creando archivo de configuración..."
    cp config.example.ini config.ini
    echo "✅ Archivo config.ini creado"
    echo ""
    echo "⚠️  IMPORTANTE: Edita config.ini y añade tu token de Telegram"
    echo ""
    echo "Para obtener un token:"
    echo "1. Habla con @BotFather en Telegram"
    echo "2. Usa /newbot y sigue las instrucciones"
    echo "3. Copia el token en config.ini"
    echo ""
else
    echo "✅ config.ini ya existe"
    echo ""
fi

echo "🎉 Instalación completada!"
echo ""
echo "Para iniciar el bot:"
echo "1. Edita config.ini con tu configuración"
echo "2. Ejecuta: source venv/bin/activate"
echo "3. Ejecuta: python bot.py"
echo ""
echo "O usa el script de inicio:"
echo "  ./start.sh"
echo ""
