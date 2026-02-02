#!/bin/bash
# reComm - Szybka instalacja dla openSUSE
# Uruchom: curl -sSL [url]/install.sh | bash

set -e

echo "=== reComm Instalator ==="
echo ""

# Sprawdzenie systemu
if ! grep -qi "suse" /etc/os-release 2>/dev/null; then
    echo "UWAGA: Ten skrypt jest przeznaczony dla openSUSE"
fi

# Instalacja zależności systemowych
echo ">>> Instalacja zależności systemowych..."
sudo zypper install -y python312 python312-pip python312-tkinter git

# Pobranie kodu (jeśli nie istnieje)
if [ ! -d "reComm" ]; then
    echo ">>> Pobieranie repozytorium..."
    git clone https://github.com/[twoje-repo]/reComm.git
fi

cd reComm/frontend

# Utworzenie środowiska
echo ">>> Konfiguracja środowiska Python..."
python3.12 -m venv .venv
source .venv/bin/activate

# Instalacja pakietów Python
echo ">>> Instalacja pakietów Python..."
pip install --upgrade pip
pip install customtkinter pillow pydantic

echo ""
echo "=== INSTALACJA ZAKOŃCZONA ==="
echo ""
echo "Uruchom aplikację:"
echo "  cd reComm/frontend"
echo "  source .venv/bin/activate"
echo "  python main.py"
