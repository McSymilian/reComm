# reComm

Aplikacja serwerowa dla systemu reComm w C++20 z obsługą użytkowników, znajomych i grup z desktopowym clientem napisanym w python 3.12 przy pomocy PyQT6

## Funkcjonalności

- ✅ Rejestracja i autentykacja użytkowników (JWT)
- ✅ System znajomych (wysyłanie/akceptowanie zaproszeń)
- ✅ System grup:
  - Tworzenie grup
  - Dodawanie znajomych do grup (tylko członkowie)
  - Zmiana nazwy grupy (każdy członek)
  - Opuszczanie grupy
  - Usuwanie grupy
- ✅ System wiadomości:
  - **Wiadomości grupowe:**
    - Wysyłanie wiadomości do grup
    - Pobieranie historii wiadomości z paginacją
    - Filtrowanie wiadomości po czasie
  - **Wiadomości prywatne:**
    - Wysyłanie wiadomości do znajomych
    - Pobieranie historii konwersacji prywatnych
    - Paginacja i filtrowanie
  - **Live delivery:**
    - Natychmiastowe dostarczanie wiadomości do połączonych użytkowników
    - Notyfikacje NEW_GROUP_MESSAGE i NEW_PRIVATE_MESSAGE
- ✅ Powiadomienia w czasie rzeczywistym
- ✅ Przechowywanie danych w plikach JSON


## Wymagania systemowe

- System operacyjny: Linux (Ubuntu 20.04+, openSUSE Leap 15.3+)
- Kompilator: GCC 14+ z obsługą C++20
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

