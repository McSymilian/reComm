# reComm Backend

Aplikacja serwerowa dla systemu reComm w C++20 z obsługą użytkowników, znajomych i grup.

## Funkcjonalności

- ✅ Rejestracja i autentykacja użytkowników (JWT)
- ✅ System znajomych (wysyłanie/akceptowanie zaproszeń)
- ✅ System grup:
  - Tworzenie grup
  - Dodawanie znajomych do grup (tylko członkowie)
  - Zmiana nazwy grupy (każdy członek)
  - Opuszczanie grupy
  - Usuwanie grupy
- ✅ Powiadomienia w czasie rzeczywistym
- ✅ Przechowywanie danych w plikach JSON


## Instalacja

### Ubuntu (20.04 LTS i nowsze)

```bash
# Aktualizacja repozytoriów
sudo apt update

# Instalacja kompilatora C++20 (GCC 10 lub nowszy)
sudo apt install -y build-essential g++-10

# Ustawienie GCC 10 jako domyślnego kompilatora
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 100

# Instalacja CMake (wersja 3.16 lub nowsza)
sudo apt install -y cmake

# Instalacja Make
sudo apt install -y make

# Instalacja OpenSSL (wymagane dla funkcji kryptograficznych)
sudo apt install -y libssl-dev

# Weryfikacja wersji
gcc --version    # Powinno pokazać GCC 10.x lub nowszy
cmake --version  # Powinno pokazać CMake 3.16.x lub nowszy
make --version
openssl version  # Powinno pokazać OpenSSL 1.0.1 lub nowszy
```

### openSUSE Leap (15.3 i nowsze)

```bash
# Aktualizacja repozytoriów
sudo zypper refresh

# Instalacja kompilatora C++20 (GCC 10 lub nowszy)
sudo zypper install -y gcc10 gcc10-c++

# Ustawienie GCC 10 jako domyślnego kompilatora
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 100

# Instalacja CMake
sudo zypper install -y cmake

# Instalacja Make
sudo zypper install -y make

# Instalacja OpenSSL (wymagane dla funkcji kryptograficznych)
sudo zypper install -y libopenssl-devel

# Weryfikacja wersji
gcc --version    # Powinno pokazać GCC 10.x lub nowszy
cmake --version
make --version
openssl version  # Powinno pokazać OpenSSL 1.0.1 lub nowszy
```

### Budowanie projektu

```bash
# Przejście do katalogu projektu
cd reComm/backend/

# Utworzenie katalogu build
mkdir build && cd build

# Generowanie plików Make za pomocą CMake
cmake ..

# Kompilacja
make

# Uruchomienie aplikacji
./reComm
```

## Wymagania systemowe

- System operacyjny: Linux (Ubuntu 20.04+, openSUSE Leap 15.3+)
- Kompilator: GCC 10+ z obsługą C++20
- CMake: 3.16+
- Make
- OpenSSL: 1.1.1+ (biblioteki deweloperskie)

## Architektura systemu powiadomień

### Komponenty:

#### 1. **ConnectionManager** (`src/infrastructure/ConnectionManager.h`)
Zarządza aktywnymi połączeniami TCP klientów.
- Przechowuje mapę: `userId → socket`
- Thread-safe dzięki mutex'om
- Umożliwia wysyłanie wiadomości do konkretnego użytkownika

#### 2. **NotificationService** (`src/application/NotificationService.h`)
Logika biznesowa dla powiadomień.
- Sprawdza czy użytkownik jest online
- Wysyła powiadomienie live lub zapisuje do kolejki
- Wysyła zaległe powiadomienia przy logowaniu

#### 3. **NotificationRepository** (`src/domain/notification/NotificationRepository.h`)
Interfejs dla przechowywania zaległych powiadomień.

#### 4. **FileNotificationRepository** (`src/infrastructure/FileNotificationRepository.h`)
Implementacja zapisująca powiadomienia do plików JSON.
- Format: `db/notifications_{userId}.json`
- Thread-safe operacje na plikach

### Przepływ danych:

```
Użytkownik A wysyła zaproszenie do Użytkownika B
                 ↓
       SendFriendRequestService
                 ↓
         NotificationService
                 ↓
        ┌────────────────────┐
        │ Czy B jest online? │
        └────────┬───────────┘
                 │
        ┌────────┴────────┐
        │                 │
       TAK               NIE
        │                 │
  ConnectionManager   FileNotificationRepository
        │                 │
  Wysłanie przez     Zapisanie do pliku
     socket             (kolejka)
        │                 │
        ↓                 ↓
  B otrzymuje           B otrzyma przy
  natychmiast          następnym logowaniu
```

### Bezpieczeństwo wątkowe:

- **ConnectionManager**: mutex na mapę połączeń + mutex per-connection
- **FileNotificationRepository**: mutex na operacje plikowe
- **NotificationService**: używa thread-safe komponentów

### Persistent Connections:

Serwer utrzymuje otwarte połączenia TCP z klientami:
- Jedno połączenie obsługuje wiele żądań API
- Połączenie pozostaje otwarte po zalogowaniu
- Serwer może wysyłać powiadomienia w dowolnym momencie
- Połączenie zamykane tylko przy:
  - Rozłączeniu klienta
  - Błędzie sieci
  - Wewnętrznym błędzie serwera

