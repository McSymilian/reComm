# Dokumentacja JSON API - reComm Backend

Kompletna dokumentacja REST-like JSON API dla systemu reComm.

## 📚 Spis treści

### Dokumentacja ogólna
- **[API_OVERVIEW.md](API_OVERVIEW.md)** - Przegląd API, format komunikacji, autentykacja, powiadomienia, bezpieczeństwo

### Dokumentacja endpointów

#### Autentykacja
- **[API_AUTH.md](API_AUTH.md)** - `AUTH` - Logowanie użytkownika
- **[API_REGISTER.md](API_REGISTER.md)** - `REGISTER` - Rejestracja nowego użytkownika

#### System znajomych
- **[API_FRIENDS.md](API_FRIENDS.md)** - Kompletna dokumentacja systemu znajomych:
  - `SEND_FRIEND_REQUEST` - Wysłanie zaproszenia
  - `ACCEPT_FRIEND_REQUEST` - Akceptowanie zaproszenia
  - `REJECT_FRIEND_REQUEST` - Odrzucenie zaproszenia
  - `GET_FRIENDS` - Lista znajomych
  - `GET_PENDING_REQUESTS` - Oczekujące zaproszenia

#### System grup
- **[API_GROUPS.md](API_GROUPS.md)** - Kompletna dokumentacja systemu grup:
  - `CREATE_GROUP` - Utworzenie grupy
  - `ADD_MEMBER_TO_GROUP` - Dodanie członka do grupy
  - `UPDATE_GROUP_NAME` - Zmiana nazwy grupy
  - `LEAVE_GROUP` - Opuszczenie grupy
  - `DELETE_GROUP` - Usunięcie grupy
  - `GET_USER_GROUPS` - Lista grup użytkownika
  - `GET_GROUP_DETAILS` - Szczegóły grupy
  - `GET_GROUP_MEMBERS` - Lista członków grupy

---

## 🚀 Szybki start

### 1. Rejestracja użytkownika

```bash
echo '{"method":"REGISTER","body":{"username":"jan","password":"haslo123"}}' | nc localhost 8080
```

**Odpowiedź:**
```json
{
  "code": 201,
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Logowanie

```bash
echo '{"method":"AUTH","body":{"username":"jan","password":"haslo123"}}' | nc localhost 8080
```

**Odpowiedź:**
```json
{
  "code": 200,
  "message": "Authenticated",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Wysłanie zaproszenia do znajomych

```bash
echo '{"method":"SEND_FRIEND_REQUEST","body":{"token":"TWOJ_TOKEN","addresseeUsername":"anna"}}' | nc localhost 8080
```

### 4. Utworzenie grupy

```bash
echo '{"method":"CREATE_GROUP","body":{"token":"TWOJ_TOKEN","groupName":"Moja grupa"}}' | nc localhost 8080
```

---

## 📋 Lista wszystkich metod

| Metoda | Autentykacja | Opis | Dokumentacja |
|--------|--------------|------|--------------|
| `REGISTER` | ❌ | Rejestracja nowego użytkownika | [API_REGISTER.md](API_REGISTER.md) |
| `AUTH` | ❌ | Logowanie użytkownika | [API_AUTH.md](API_AUTH.md) |
| `SEND_FRIEND_REQUEST` | ✅ | Wysłanie zaproszenia do znajomych | [API_FRIENDS.md](API_FRIENDS.md#send_friend_request) |
| `ACCEPT_FRIEND_REQUEST` | ✅ | Akceptowanie zaproszenia | [API_FRIENDS.md](API_FRIENDS.md#accept_friend_request) |
| `REJECT_FRIEND_REQUEST` | ✅ | Odrzucenie zaproszenia | [API_FRIENDS.md](API_FRIENDS.md#reject_friend_request) |
| `GET_FRIENDS` | ✅ | Lista znajomych | [API_FRIENDS.md](API_FRIENDS.md#get_friends) |
| `GET_PENDING_REQUESTS` | ✅ | Oczekujące zaproszenia | [API_FRIENDS.md](API_FRIENDS.md#get_pending_requests) |
| `CREATE_GROUP` | ✅ | Utworzenie grupy | [API_GROUPS.md](API_GROUPS.md#create_group) |
| `ADD_MEMBER_TO_GROUP` | ✅ | Dodanie członka do grupy | [API_GROUPS.md](API_GROUPS.md#add_member_to_group) |
| `UPDATE_GROUP_NAME` | ✅ | Zmiana nazwy grupy | [API_GROUPS.md](API_GROUPS.md#update_group_name) |
| `LEAVE_GROUP` | ✅ | Opuszczenie grupy | [API_GROUPS.md](API_GROUPS.md#leave_group) |
| `DELETE_GROUP` | ✅ | Usunięcie grupy | [API_GROUPS.md](API_GROUPS.md#delete_group) |
| `GET_USER_GROUPS` | ✅ | Lista grup użytkownika | [API_GROUPS.md](API_GROUPS.md#get_user_groups) |
| `GET_GROUP_DETAILS` | ✅ | Szczegóły grupy | [API_GROUPS.md](API_GROUPS.md#get_group_details) |
| `GET_GROUP_MEMBERS` | ✅ | Lista członków grupy | [API_GROUPS.md](API_GROUPS.md#get_group_members) |

---

## 🔔 Powiadomienia Push

System obsługuje powiadomienia w czasie rzeczywistym przez te same połączenia TCP.

**Typy powiadomień:**
- `FRIEND_REQUEST` - Nowe zaproszenie do znajomych

**Przykład:**
```json
{
  "type": "FRIEND_REQUEST",
  "from": "jan",
  "message": "You have a new friend request"
}
```

Więcej informacji: [API_OVERVIEW.md - Powiadomienia Push](API_OVERVIEW.md#powiadomienia-push)

---

## 🔐 Autentykacja

Metody wymagające autentykacji potrzebują **tokenu JWT** w polu `token` żądania.

**Przykład:**
```json
{
  "method": "GET_FRIENDS",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {}
}
```

Token otrzymujesz po:
- Rejestracji (`REGISTER`)
- Logowaniu (`AUTH`)

Token jest ważny przez **12 godzin**.

Więcej informacji: [API_OVERVIEW.md - Autentykacja](API_OVERVIEW.md#autentykacja)

---

## ⚠️ Kody odpowiedzi

| Kod | Znaczenie | Opis |
|-----|-----------|------|
| `200` | OK | Operacja zakończona sukcesem |
| `201` | Created | Zasób utworzony (rejestracja) |
| `400` | Bad Request | Błędne żądanie |
| `401` | Unauthorized | Brak autoryzacji |
| `403` | Forbidden | Brak uprawnień |
| `404` | Not Found | Zasób nie znaleziony |
| `409` | Conflict | Konflikt (np. użytkownik istnieje) |
| `500` | Internal Server Error | Błąd serwera |

---

## 🛠️ Testowanie

### Netcat (nc)

**Pojedyncze żądanie:**
```bash
echo '{"method":"AUTH","body":{"username":"jan","password":"pass"}}' | nc localhost 8080
```

**Interaktywnie (wiele żądań):**
```bash
nc localhost 8080
{"method":"REGISTER","body":{"username":"test","password":"pass"}}
{"method":"GET_FRIENDS","token":"otrzymany_token","body":{}}
```

### Python

```python
import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))

request = {
    "method": "AUTH",
    "body": {
        "username": "jan",
        "password": "pass"
    }
}

sock.sendall((json.dumps(request) + "\n").encode())
response = sock.recv(4096).decode()
print(json.loads(response))
```

### Skrypt testowy

```bash
./test_groups.sh
```

Kompleksowy test wszystkich funkcjonalności.

---

## 📖 Struktura dokumentacji

Każdy plik dokumentacji zawiera:

- **Opis metody** - co robi
- **Wymagana autentykacja** - czy potrzebny token
- **Żądanie** - przykład JSON
- **Parametry** - tabela z opisem
- **Odpowiedzi** - wszystkie możliwe kody odpowiedzi z przykładami
- **Przykłady użycia** - praktyczne przykłady
- **Scenariusze** - typowe przypadki użycia

---


## 📞 Wsparcie

Dla problemów lub pytań dotyczących API:
1. Sprawdź odpowiedni plik dokumentacji
2. Zobacz [API_OVERVIEW.md](API_OVERVIEW.md) dla ogólnych informacji

---

## 📝 Notatki

- Wszystkie żądania i odpowiedzi są w formacie **JSON**
- Połączenia TCP są **długotrwałe** (persistent)
- Powiadomienia wysyłane są **push** przez ten sam socket
- Token JWT jest ważny **12 godziny**
- Hasła są **hashowane** za pomocą bcrypt
- Dane przechowywane w plikach **JSON** w katalogu `db/`

---

**Wersja dokumentacji:** 1.0  
**Data ostatniej aktualizacji:** 2025-01-23  
**Zgodność z wersją backendu:** reComm 1.0

