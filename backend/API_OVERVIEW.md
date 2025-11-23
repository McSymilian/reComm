# API - Ogólne informacje

## Format komunikacji

Wszystkie żądania i odpowiedzi są w formacie JSON.

### Format żądania
```json
{
  "method": "NAZWA_METODY",
  "body": {
    // parametry specyficzne dla metody
  }
}
```

### Format odpowiedzi
```json
{
  "code": 200,
  "message": "Success message",
  // dodatkowe pola zależne od metody
}
```

---

## Kody odpowiedzi HTTP

| Kod | Znaczenie | Opis |
|-----|-----------|------|
| `200` | OK | Operacja zakończona sukcesem |
| `201` | Created | Zasób utworzony pomyślnie (np. rejestracja) |
| `400` | Bad Request | Błędne żądanie (brak pól, nieprawidłowy format) |
| `401` | Unauthorized | Brak autoryzacji lub nieprawidłowy token |
| `403` | Forbidden | Brak uprawnień do wykonania operacji |
| `404` | Not Found | Zasób nie znaleziony |
| `409` | Conflict | Konflikt (np. użytkownik już istnieje) |
| `500` | Internal Server Error | Błąd wewnętrzny serwera |

---

## Autentykacja

### Token JWT

Po zalogowaniu lub rejestracji użytkownik otrzymuje token JWT, który musi być używany w każdym żądaniu wymagającym autentykacji.

**Struktura tokenu:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI0MDk2MDAsImlhdCI6MTczMjMyMzIwMCwiaXNzIjoicmVDb21tIiwidXVpZCI6IjEyMzQ1Njc4LTkwYWItY2RlZi0xMjM0LTU2Nzg5MGFiY2RlZiJ9.signature
```

**Zawartość (payload):**
```json
{
  "exp": 1732409600,
  "iat": 1732323200,
  "iss": "reComm",
  "uuid": "12345678-90ab-cdef-1234-567890abcdef"
}
```

- `exp` - data wygaśnięcia (timestamp Unix)
- `iat` - data wystawienia (timestamp Unix)
- `iss` - wystawca (zawsze "reComm")
- `uuid` - UUID użytkownika

**Ważność:** Token jest ważny przez **24 godziny** od momentu wystawienia.

### Użycie tokenu

Token musi być przekazany w polu `token` żądania:

```json
{
  "method": "NAZWA_METODY",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    // inne parametry
  }
}
```

---

## Obsługa błędów

### Błędy wspólne dla wszystkich metod

#### Zły format żądania
```json
{
  "code": 400,
  "message": "Bad request format"
}
```

#### Nieznana metoda
```json
{
  "code": 400,
  "message": "Unknown method: NAZWA_METODY"
}
```

#### Brakujące pole wymagane
```json
{
  "code": 400,
  "message": "Missing required field: nazwa_pola"
}
```

#### Nieprawidłowy lub wygasły token
```json
{
  "code": 401,
  "message": "Invalid or expired token"
}
```

#### Brak autoryzacji
```json
{
  "code": 401,
  "message": "Unauthorized"
}
```

#### Błąd wewnętrzny serwera
```json
{
  "code": 500,
  "message": "Internal server error"
}
```

---

## Połączenia TCP

### Persistent Connections

Serwer utrzymuje **długotrwałe połączenia TCP** z klientami:

1. **Jedno połączenie** - obsługuje wiele żądań
2. **Pozostaje otwarte** - po zalogowaniu/rejestracji
3. **Dwukierunkowe** - klient wysyła żądania, serwer wysyła odpowiedzi i powiadomienia

### Jak działa:

```
Klient                          Serwer
  |                               |
  |---- 1. Nawiązanie TCP ------->|
  |                               |
  |---- 2. REGISTER/AUTH -------->|
  |<---- Token JWT ---------------|
  |                               |
  |---- 3. Inne żądania --------->|
  |<---- Odpowiedzi --------------|
  |                               |
  |<---- Powiadomienia (push) ----|
  |                               |
  |---- 4. Kolejne żądania ------>|
  |<---- Odpowiedzi --------------|
  |                               |
```

### Zamknięcie połączenia

Połączenie jest zamykane gdy:
- Klient rozłącza się
- Błąd sieci
- Wewnętrzny błąd serwera
- Błąd parsowania JSON (w niektórych przypadkach)

---

## Powiadomienia Push

### Mechanizm

Serwer może **w dowolnym momencie** wysłać powiadomienie do zalogowanego użytkownika przez to samo połączenie TCP.

### Format powiadomienia

```json
{
  "type": "TYP_POWIADOMIENIA",
  "from": "nadawca",
  "message": "Treść powiadomienia"
}
```

### Typy powiadomień

| Typ | Opis | Kiedy wysyłane |
|-----|------|----------------|
| `FRIEND_REQUEST` | Zaproszenie do znajomych | Gdy ktoś wyśle zaproszenie |

### Przykład powiadomienia

```json
{
  "type": "FRIEND_REQUEST",
  "from": "jan",
  "message": "You have a new friend request"
}
```

### Kolejka powiadomień

#### Użytkownik online
- Powiadomienie wysyłane **natychmiast** przez otwarty socket

#### Użytkownik offline
- Powiadomienie zapisywane w **kolejce** (plik `db/notifications_{userId}.json`)
- Wysyłane **automatycznie** przy następnym logowaniu
- Usuwane z kolejki po wysłaniu

### Implementacja klienta

Klient musi:
1. **Utrzymywać otwarte połączenie** po zalogowaniu
2. **Nasłuchiwać asynchronicznie** na dane z socketa
3. **Rozróżniać** powiadomienia od odpowiedzi na żądania

**Rozpoznawanie:**
- **Powiadomienie:** ma pole `type`
- **Odpowiedź na żądanie:** ma pole `code`

**Przykład (Python):**
```python
import socket
import json
import threading

def receive_messages(sock):
    while True:
        data = sock.recv(4096).decode()
        if not data:
            break
        
        message = json.loads(data)
        
        if "type" in message:
            # To powiadomienie push
            print(f"🔔 Powiadomienie: {message}")
        elif "code" in message:
            # To odpowiedź na żądanie
            print(f"✅ Odpowiedź: {message}")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))

# Wątek nasłuchujący
receiver = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
receiver.start()

# Logowanie
login = {"method": "AUTH", "body": {"username": "jan", "password": "pass"}}
sock.sendall((json.dumps(login) + "\n").encode())

# Teraz możesz wysyłać żądania i otrzymywać powiadomienia jednocześnie
```

---

## Limity i ograniczenia

| Parametr | Wartość            |
|----------|--------------------|
| Rozmiar bufora żądania | 4096 bajtów        |
| Ważność tokenu JWT | 12 godziny         |
| Maksymalna długość username | Brak (praktycznie) |
| Maksymalna długość nazwy grupy | Brak (praktycznie) |

---

## Bezpieczeństwo

### Hasła
- Hashowane za pomocą **bcrypt**
- Nie są nigdy zwracane w odpowiedziach API
- Nie są logowane

### Tokeny JWT
- Podpisane kluczem tajnym serwera
- Zawierają UUID użytkownika
- Mają określony czas wygaśnięcia (12h)
- Weryfikowane przy każdym żądaniu wymagającym autentykacji

### Logowanie
Wszystkie operacje są logowane z poziomami:
- **INFO** - normalne operacje
- **WARNING** - potencjalne problemy
- **ERROR** - błędy wymagające uwagi

### Połączenia
- Każde połączenie jest identyfikowane przez IP:port
- Thread-safe operacje na współdzielonych zasobach
- Mutex'y chroniące dostęp do mapy połączeń

---

## Przechowywanie danych

### Struktura katalogów

```
db/
├── users.json              # Baza użytkowników
├── friendships.json        # Relacje znajomości
├── groups.json             # Grupy
├── notifications_{uuid}.json  # Kolejka powiadomień per użytkownik
```

### Format plików

Wszystkie dane przechowywane są w formacie **JSON**.

**users.json:**
```json
[
  {
    "uuid": "12345678-90ab-cdef-1234-567890abcdef",
    "username": "jan",
    "passwordHash": "$2b$10$...",
    "createdAt": "2025-01-15T10:30:00Z"
  }
]
```

**friendships.json:**
```json
[
  {
    "requesterId": "uuid1",
    "addresseeId": "uuid2",
    "status": 1,
    "createdAt": "2025-01-15T10:30:00Z"
  }
]
```

**groups.json:**
```json
[
  {
    "id": "group-uuid",
    "name": "Grupa testowa",
    "creatorId": "user-uuid",
    "memberIds": ["uuid1", "uuid2"],
    "createdAt": "2025-01-15T10:30:00Z"
  }
]
```

---

## Testowanie API

### Narzędzia

- **netcat (nc)** - prosty klient TCP
- **telnet** - alternatywa dla netcat
- **Python socket** - dla bardziej zaawansowanych testów
- **curl** - nie działa (to nie jest HTTP)

### Przykłady z netcat

**Rejestracja:**
```bash
echo '{"method":"REGISTER","body":{"username":"test","password":"pass"}}' | nc localhost 8080
```

**Logowanie:**
```bash
echo '{"method":"AUTH","body":{"username":"test","password":"pass"}}' | nc localhost 8080
```

**Wiele żądań (interaktywnie):**
```bash
nc localhost 8080
{"method":"REGISTER","body":{"username":"test","password":"pass"}}
{"method":"GET_FRIENDS","token":"otrzymany_token","body":{}}
{"method":"SEND_FRIEND_REQUEST","token":"otrzymany_token","body":{"addresseeUsername":"jan"}}
```

### Skrypt testowy

Dostępny jest skrypt bash do kompleksowego testowania:
```bash
./test_groups.sh
```

---

## Architektura

### Komponenty

```
┌─────────────────────────────────────┐
│        main.cpp (TCP Server)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     RequestHandleService            │  Routing żądań
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┬──────────┬────────────┐
       ▼                ▼          ▼            ▼
┌────────────┐  ┌──────────┐  ┌────────┐  ┌────────┐
│ Auth       │  │ Friends  │  │ Groups │  │ Notif. │
│ Services   │  │ Services │  │Services│  │ Service│
└────────────┘  └──────────┘  └────────┘  └────────┘
       │                │          │            │
       ▼                ▼          ▼            ▼
┌────────────┐  ┌──────────┐  ┌────────┐  ┌─────────┐
│ User       │  │Friendship│  │ Group  │  │ Notif.  │
│ Service    │  │ Service  │  │ Service│  │ Repo    │
└────────────┘  └──────────┘  └────────┘  └─────────┘
       │                │          │            │
       ▼                ▼          ▼            ▼
┌────────────┐  ┌──────────┐  ┌────────┐  ┌─────────┐
│ User Repo  │  │Friendship│  │ Group  │  │ File    │
│ (File)     │  │ Repo     │  │ Repo   │  │ Storage │
└────────────┘  └──────────┘  └────────┘  └─────────┘
```

### Wzorce projektowe

- **Repository Pattern** - abstrakcja dostępu do danych
- **Service Layer** - logika biznesowa
- **Dependency Injection** - przez konstruktory
- **Strategy Pattern** - różne handlery dla różnych metod

---

## Wsparcie

Dla szczegółowej dokumentacji poszczególnych grup metod, zobacz:

- **[API_AUTH.md](API_AUTH.md)** - Autentykacja (AUTH)
- **[API_REGISTER.md](API_REGISTER.md)** - Rejestracja (REGISTER)
- **[API_FRIENDS.md](API_FRIENDS.md)** - System znajomych
- **[API_GROUPS.md](API_GROUPS.md)** - System grup

