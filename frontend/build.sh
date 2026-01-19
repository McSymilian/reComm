#!/bin/bash
# reComm - Skrypt budowania dla openSUSE Linux
# Uruchom: chmod +x build.sh && ./build.sh

set -e

echo "=== reComm Build Script ==="
echo ""

# Sprawdzenie Pythona
if ! command -v python3 &> /dev/null; then
    echo "BŁĄD: Python3 nie jest zainstalowany"
    echo "Zainstaluj: sudo zypper install python312"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Znaleziono Python $PYTHON_VERSION"

# Utworzenie środowiska wirtualnego
echo ""
echo ">>> Tworzenie środowiska wirtualnego..."
python3 -m venv .build_venv
source .build_venv/bin/activate

# Instalacja zależności
echo ""
echo ">>> Instalacja zależności..."
pip install --upgrade pip
pip install customtkinter pillow pydantic pyinstaller

# Budowanie
echo ""
echo ">>> Budowanie aplikacji..."
pyinstaller --onefile \
    --name reComm \
    --add-data "src:src" \
    --hidden-import customtkinter \
    --hidden-import PIL \
    --hidden-import PIL._tkinter_finder \
    --hidden-import pydantic \
    --hidden-import pydantic_core \
    --collect-all customtkinter \
    --noconsole \
    main.py

# Czyszczenie
echo ""
echo ">>> Czyszczenie..."
rm -rf build/ *.spec .build_venv/

echo ""
echo "=== SUKCES ==="
echo "Plik wykonywalny: dist/reComm"
echo ""
echo "Uruchom: ./dist/reComm"
