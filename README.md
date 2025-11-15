# reComm Backend

Aplikacja serwerowa dla systemu reComm w C++20.

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
openssl version  # Powinno pokazać OpenSSL 1.1.1 lub nowszy
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
openssl version  # Powinno pokazać OpenSSL 1.1.1 lub nowszy
```

### Budowanie projektu

```bash
# Przejście do katalogu projektu
cd reComm

# Utworzenie katalogu build
mkdir build && cd build

# Generowanie plików Make za pomocą CMake
cmake ..

# Kompilacja
make

# Uruchomienie aplikacji
./reComm
```

## API

### Format żądania

Wszystkie żądania muszą być w formacie JSON:

```json
{
  "method": "NAZWA_METODY",
  "body": {
    // parametry specyficzne dla metody
  }
}
```

### Dostępne metody

#### 1. REGISTER - Rejestracja nowego użytkownika

**Żądanie:**
```json
{
  "method": "REGISTER",
  "body": {
    "username": "nazwa_uzytkownika",
    "password": "haslo"
  }
}
```

**Odpowiedzi:**

Sukces (201):
```json
{
  "code": 201,
  "message": "User registered successfully",
  "token": "wygenerowany_token_autentykacji"
}
```

Użytkownik już istnieje (409):
```json
{
  "code": 409,
  "message": "Username is already taken"
}
```

#### 2. AUTH - Autentykacja użytkownika

**Żądanie:**
```json
{
  "method": "AUTH",
  "body": {
    "username": "nazwa_uzytkownika",
    "password": "haslo"
  }
}
```

**Odpowiedzi:**

Sukces (200):
```json
{
  "code": 200,
  "message": "Authenticated",
  "token": "wygenerowany_token_autentykacji"
}
```

Nieprawidłowe dane (401):
```json
{
  "code": 401,
  "message": "Invalid credentials"
}
```

### Kody błędów

| Kod | Znaczenie | Opis |
|-----|-----------|------|
| 200 | OK | Żądanie zakończone sukcesem |
| 201 | Created | Zasób został utworzony |
| 400 | Bad Request | Nieprawidłowy format żądania lub nieznana metoda |
| 401 | Unauthorized | Nieprawidłowe dane uwierzytelniające |
| 409 | Conflict | Konflikt zasobów (np. użytkownik już istnieje) |
| 500 | Internal Server Error | Błąd wewnętrzny serwera |

### Ogólne błędy

**Nieprawidłowy format żądania:**
```json
{
  "code": 400,
  "message": "Bad request format"
}
```

**Nieznana metoda:**
```json
{
  "code": 400,
  "message": "Unknown method: NAZWA_METODY"
}
```

**Błąd wewnętrzny:**
```json
{
  "code": 500,
  "message": "Internal server error"
}
```

## Wymagania systemowe

- System operacyjny: Linux (Ubuntu 20.04+, openSUSE Leap 15.3+)
- Kompilator: GCC 10+ z obsługą C++20
- CMake: 3.16+
- Make
- OpenSSL: 1.1.1+ (biblioteki deweloperskie)
