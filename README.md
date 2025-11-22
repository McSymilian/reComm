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

#### 3. SEND_FRIEND_REQUEST - Wysłanie zaproszenia do znajomych

**Żądanie:**
```json
{
  "method": "SEND_FRIEND_REQUEST",
  "body": {
    "token": "token_autentykacji",
    "addresseeUsername": "nazwa_uzytkownika_odbiorcy"
  }
}
```

**Odpowiedzi:**

Sukces (200):
```json
{
  "code": 200,
  "message": "Friend request sent successfully"
}
```

Nieprawidłowy token (401):
```json
{
  "code": 401,
  "message": "Invalid or expired token"
}
```

Użytkownik nie znaleziony (404):
```json
{
  "code": 404,
  "message": "User not found"
}
```

Próba dodania siebie (400):
```json
{
  "code": 400,
  "message": "Cannot add yourself as a friend"
}
```

Już są znajomymi (409):
```json
{
  "code": 409,
  "message": "Accounts are already friends"
}
```

Zaproszenie już wysłane (409):
```json
{
  "code": 409,
  "message": "Friend request already sent"
}
```

#### 4. ACCEPT_FRIEND_REQUEST - Akceptowanie zaproszenia do znajomych

**Żądanie:**
```json
{
  "method": "ACCEPT_FRIEND_REQUEST",
  "body": {
    "token": "token_autentykacji",
    "requesterUuid": "uuid_uzytkownika_wysylajacego"
  }
}
```

**Odpowiedzi:**

Sukces (200):
```json
{
  "code": 200,
  "message": "Friend request accepted"
}
```

Nieprawidłowy token (401):
```json
{
  "code": 401,
  "message": "Invalid or expired token"
}
```

Zaproszenie nie znalezione (404):
```json
{
  "code": 404,
  "message": "Friend request not found"
}
```

Zaproszenie już przetworzone (409):
```json
{
  "code": 409,
  "message": "Friend request already processed"
}
```

#### 5. REJECT_FRIEND_REQUEST - Odrzucenie zaproszenia do znajomych

**Żądanie:**
```json
{
  "method": "REJECT_FRIEND_REQUEST",
  "body": {
    "token": "token_autentykacji",
    "requesterUuid": "uuid_uzytkownika_wysylajacego"
  }
}
```

**Odpowiedzi:**

Sukces (200):
```json
{
  "code": 200,
  "message": "Friend request rejected"
}
```

Nieprawidłowy token (401):
```json
{
  "code": 401,
  "message": "Invalid or expired token"
}
```

Zaproszenie nie znalezione (404):
```json
{
  "code": 404,
  "message": "Friend request not found"
}
```

Zaproszenie już przetworzone (409):
```json
{
  "code": 409,
  "message": "Friend request already processed"
}
```

#### 6. GET_FRIENDS - Pobieranie listy znajomych

**Żądanie:**
```json
{
  "method": "GET_FRIENDS",
  "body": {
    "token": "token_autentykacji"
  }
}
```

**Odpowiedzi:**

Sukces (200):
```json
{
  "code": 200,
  "message": "Friends retrieved successfully",
  "friends": [
    "uuid_znajomego_1",
    "uuid_znajomego_2",
    "uuid_znajomego_3"
  ]
}
```

Nieprawidłowy token (401):
```json
{
  "code": 401,
  "message": "Invalid or expired token"
}
```

#### 7. GET_PENDING_REQUESTS - Pobieranie oczekujących zaproszeń

**Żądanie:**
```json
{
  "method": "GET_PENDING_REQUESTS",
  "body": {
    "token": "token_autentykacji"
  }
}
```

**Odpowiedzi:**

Sukces (200):
```json
{
  "code": 200,
  "message": "Pending requests retrieved successfully",
  "pendingRequests": [
    {
      "requesterId": "uuid_nadawcy",
      "addresseeId": "uuid_odbiorcy",
      "status": 0
    }
  ]
}
```

**Uwaga:** Status przyjmuje wartości:
- `0` - PENDING (oczekujące)
- `1` - ACCEPTED (zaakceptowane)
- `2` - REJECTED (odrzucone)

Nieprawidłowy token (401):
```json
{
  "code": 401,
  "message": "Invalid or expired token"
}
```

### Powiadomienia Push (Server-Sent Notifications)

Serwer automatycznie wysyła powiadomienia do zalogowanych użytkowników w czasie rzeczywistym. Powiadomienia są wysyłane przez to samo połączenie TCP, które jest używane do komunikacji z API.

#### Jak działają powiadomienia:

1. **Użytkownik online** - otrzymuje powiadomienie natychmiast przez otwarty socket
2. **Użytkownik offline** - powiadomienie jest zapisywane i wysyłane przy następnym logowaniu

#### Format powiadomień:

Po zalogowaniu (AUTH lub REGISTER), klient może otrzymywać powiadomienia push w formacie JSON:

**Powiadomienie o zaproszeniu do znajomych:**
```json
{
  "type": "FRIEND_REQUEST",
  "from": "uuid_nadawcy",
  "message": "You have a new friend request"
}
```

#### Implementacja po stronie klienta:

Klient musi:
1. Utrzymywać otwarte połączenie TCP po zalogowaniu
2. Nasłuchiwać na dane z socketa w osobnym wątku/asynchronicznie
3. Odróżniać powiadomienia od odpowiedzi na żądania (sprawdzając pole `type`)

**Przykład (Python):**
```python
import socket
import json
import threading

def receive_messages(sock):
    """Wątek odbierający wiadomości od serwera"""
    while True:
        try:
            data = sock.recv(4096).decode()
            if not data:
                break
            
            message = json.loads(data)
            
            # Sprawdź czy to powiadomienie push
            if message.get("type") == "FRIEND_REQUEST":
                print(f"🔔 Nowe zaproszenie od: {message['from']}")
            elif message.get("code"):
                # To odpowiedź na żądanie API
                print(f"Odpowiedź: {message}")
        except Exception as e:
            print(f"Błąd: {e}")
            break

# Nawiązanie połączenia
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))

# Uruchomienie wątku dla odbierania wiadomości
receiver_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
receiver_thread.start()

# Logowanie
login_request = {
    "method": "AUTH",
    "body": {"username": "jan", "password": "pass123"}
}
sock.sendall((json.dumps(login_request) + "\n").encode())

# Po zalogowaniu:
# 1. Otrzymasz odpowiedź na logowanie z tokenem
# 2. Otrzymasz wszystkie zaległe powiadomienia (jeśli były)
# 3. Będziesz otrzymywać powiadomienia w czasie rzeczywistym

# Teraz możesz wysyłać kolejne żądania przez ten sam socket
# i jednocześnie odbierać powiadomienia
```

#### Typy powiadomień:

| Typ | Opis | Kiedy wysyłane |
|-----|------|----------------|
| `FRIEND_REQUEST` | Zaproszenie do znajomych | Gdy ktoś wyśle zaproszenie |

#### Ważne informacje:

- Połączenie TCP pozostaje otwarte po zalogowaniu
- Klient może wysyłać wiele żądań przez to samo połączenie
- Serwer może w dowolnym momencie wysłać powiadomienie push
- Zaległe powiadomienia są wysyłane automatycznie po zalogowaniu
- Powiadomienia są usuwane z kolejki po wysłaniu

### Ogólne odpowiedzi błędów

**Brakujące pole wymagane (400):**
```json
{
  "code": 400,
  "message": "Missing required field: nazwa_pola"
}
```

**Zły format żądania (400):**
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
        ┌───────────────────┐
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

