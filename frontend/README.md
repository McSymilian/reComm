# reComm - Aplikacja do komunikacji

Aplikacja kliencka do komunikacji w czasie rzeczywistym, zbudowana przy użyciu PyQt6.

## Wymagania systemowe

- Python 3.12 lub nowszy
- Połączenie z serwerem reComm

## Wymagane biblioteki

- PyQt6 >= 6.0.0
- pyqt6-sip

---

## Instalacja

### Windows

#### 1. Instalacja Python 3.12

1. Pobierz instalator Python 3.12 ze strony oficjalnej:
   - https://www.python.org/downloads/
   
2. Uruchom instalator i **zaznacz opcję "Add Python to PATH"**

3. Kliknij "Install Now" lub "Customize installation"

4. Po instalacji zweryfikuj w PowerShell:
   ```powershell
   python --version
   ```
   Powinno wyświetlić: `Python 3.12.x`

#### 2. Instalacja zależności

Otwórz PowerShell i przejdź do katalogu projektu:

```powershell
cd C:\ścieżka\do\reComm\frontend
```

Zainstaluj wymagane biblioteki:

```powershell
pip install -r requirements.txt
```

Lub ręcznie:

```powershell
pip install PyQt6 pyqt6-sip
```

#### 3. Uruchomienie aplikacji

```powershell
cd C:\ścieżka\do\reComm\frontend
python main.py
```

---

### macOS (Apple)

#### 1. Instalacja Python 3.12

**Opcja A - Homebrew (zalecane):**

1. Zainstaluj Homebrew (jeśli nie masz):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Zainstaluj Python 3.12:
   ```bash
   brew install python@3.12
   ```

3. Zweryfikuj instalację:
   ```bash
   python3.12 --version
   ```

**Opcja B - Oficjalny instalator:**

1. Pobierz instalator ze strony: https://www.python.org/downloads/macos/
2. Uruchom pobrany plik `.pkg` i postępuj zgodnie z instrukcjami

#### 2. Instalacja zależności

Otwórz Terminal i przejdź do katalogu projektu:

```bash
cd /ścieżka/do/reComm/frontend
```

Zainstaluj wymagane biblioteki:

```bash
pip3 install -r requirements.txt
```

Lub ręcznie:

```bash
pip3 install PyQt6 pyqt6-sip
```

#### 3. Uruchomienie aplikacji

```bash
cd /ścieżka/do/reComm/frontend
python3 main.py
```

---

### Linux openSUSE

#### 1. Instalacja Python 3.12

Otwórz terminal i wykonaj:

```bash
# Odśwież repozytoria
sudo zypper refresh

# Zainstaluj Python 3.12
sudo zypper install python312 python312-pip python312-devel

# Zweryfikuj instalację
python3.12 --version
```

Jeśli Python 3.12 nie jest dostępny w standardowych repozytoriach, dodaj repozytorium:

```bash
# Dla openSUSE Tumbleweed
sudo zypper install python312

# Dla openSUSE Leap - może być potrzebne dodatkowe repozytorium
sudo zypper addrepo https://download.opensuse.org/repositories/devel:/languages:/python/openSUSE_Leap_15.5/ python-devel
sudo zypper refresh
sudo zypper install python312 python312-pip
```

#### 2. Instalacja zależności systemowych dla PyQt6

PyQt6 wymaga dodatkowych bibliotek systemowych:

```bash
sudo zypper install libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0
sudo zypper install libGL1 libEGL1 libxcb1 libxcb-icccm4 libxcb-image0 
sudo zypper install libxcb-keysyms1 libxcb-randr0 libxcb-render-util0
sudo zypper install libxcb-shape0 libxcb-sync1 libxcb-xfixes0
```

#### 3. Instalacja zależności Python

Przejdź do katalogu projektu:

```bash
cd /ścieżka/do/reComm/frontend
```

Zainstaluj wymagane biblioteki:

```bash
pip3.12 install -r requirements.txt
```

Lub ręcznie:

```bash
pip3.12 install PyQt6 pyqt6-sip
```

#### 4. Uruchomienie aplikacji

```bash
cd /ścieżka/do/reComm/frontend
python3.12 main.py
```

---

## Rozwiązywanie problemów

### Windows

**Problem:** `python` nie jest rozpoznawane jako polecenie
- **Rozwiązanie:** Upewnij się, że podczas instalacji zaznaczyłeś "Add Python to PATH". Możesz też użyć `py` zamiast `python`.

**Problem:** Błąd instalacji PyQt6
- **Rozwiązanie:** Zaktualizuj pip: `python -m pip install --upgrade pip`

### macOS

**Problem:** Błąd "xcrun: error: invalid active developer path"
- **Rozwiązanie:** Zainstaluj Command Line Tools: `xcode-select --install`

**Problem:** PyQt6 nie działa na Apple Silicon (M1/M2/M3)
- **Rozwiązanie:** Upewnij się, że używasz natywnej wersji Pythona dla ARM64

### Linux openSUSE

**Problem:** Błąd "qt.qpa.plugin: Could not load the Qt platform plugin"
- **Rozwiązanie:** Zainstaluj brakujące biblioteki xcb:
  ```bash
  sudo zypper install libxcb-xinerama0 libxcb-cursor0
  ```

**Problem:** Błąd importu PyQt6
- **Rozwiązanie:** Upewnij się, że używasz właściwej wersji pip:
  ```bash
  python3.12 -m pip install PyQt6
  ```

---

## Użycie

1. Uruchom aplikację: `python main.py`
2. Wprowadź adres IP i port serwera
3. Kliknij "Połącz"
4. Zaloguj się lub zarejestruj nowe konto
5. Korzystaj z czatu prywatnego i grupowego

---

## Autor

Maksymilian Ryder
Antoni Maćkowiak
