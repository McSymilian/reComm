# reComm - Instrukcja Instalacji (openSUSE)

## Metoda 1: Instalacja ze źródeł (Zalecana)

### Wymagania wstępne

```bash
# Instalacja Pythona 3.12+ i niezbędnych pakietów systemowych
sudo zypper install python312 python312-pip python312-tkinter

# Opcjonalnie: instalacja tk-devel dla lepszej kompatybilności
sudo zypper install tk-devel
```

### Instalacja aplikacji

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/[twoje-repo]/reComm.git
cd reComm/frontend

# 2. Utworzenie wirtualnego środowiska
python3.12 -m venv .venv
source .venv/bin/activate

# 3. Instalacja zależności
pip install customtkinter pillow pydantic

# 4. Uruchomienie aplikacji
python main.py
```

---

## Metoda 2: Instalacja z użyciem uv (Szybsza)

```bash
# 1. Instalacja uv (menedżer pakietów)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Sklonuj repozytorium
git clone https://github.com/[twoje-repo]/reComm.git
cd reComm/frontend

# 3. Uruchomienie (uv automatycznie utworzy środowisko)
uv run main.py
```

---

## Metoda 3: Kompilacja do pliku wykonywalnego

### Przygotowanie środowiska

```bash
# Instalacja PyInstaller
pip install pyinstaller

# Opcjonalnie: nuitka dla lepszej optymalizacji
pip install nuitka
```

### Kompilacja z PyInstaller

```bash
cd reComm/frontend

# Kompilacja do pojedynczego pliku wykonywalnego
pyinstaller --onefile \
    --name reComm \
    --add-data "src:src" \
    --hidden-import customtkinter \
    --hidden-import PIL \
    --hidden-import pydantic \
    main.py

# Plik wykonywalny znajduje się w: dist/reComm
```

### Kompilacja z Nuitka (lepsza wydajność)

```bash
nuitka --standalone \
    --onefile \
    --enable-plugin=tk-inter \
    --include-package=src \
    --include-package=customtkinter \
    --include-package=pydantic \
    --output-filename=reComm \
    main.py
```

---

## Rozwiązywanie problemów

### Brak modułu tkinter
```bash
sudo zypper install python312-tkinter tk-devel
```

### Błąd importu customtkinter
```bash
# Upewnij się, że używasz właściwego środowiska
source .venv/bin/activate
pip install --force-reinstall customtkinter
```

### Problemy z WebSocket/połączeniem
- Sprawdź czy serwer jest dostępny
- Zweryfikuj adres IP i port przy uruchomieniu

---

## Szybki start (jednolinijkowiec)

```bash
# Dla systemów z uv
curl -LsSf https://astral.sh/uv/install.sh | sh && \
git clone https://github.com/[twoje-repo]/reComm.git && \
cd reComm/frontend && \
uv run main.py
```

---

## Wymagania systemowe

- **System**: openSUSE Leap 15.x / Tumbleweed
- **Python**: 3.12 lub nowszy
- **RAM**: minimum 512 MB
- **Połączenie sieciowe**: wymagane do komunikacji z serwerem
