# API Znajomych

## Przegląd

System znajomych umożliwia użytkownikom wysyłanie zaproszeń, akceptowanie/odrzucanie ich oraz zarządzanie listą znajomych.

---

## SEND_FRIEND_REQUEST - Wysłanie zaproszenia do znajomych

Wysłanie zaproszenia do innego użytkownika.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "SEND_FRIEND_REQUEST",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    "addresseeUsername": "nazwa_uzytkownika"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `addresseeUsername` | string | ✅ | Nazwa użytkownika odbiorcy |

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "message": "Friend request sent successfully"
}
```

**Powiadomienie wysłane do odbiorcy:**
```json
{
  "type": "FRIEND_REQUEST",
  "from": "nazwa_nadawcy",
  "message": "You have a new friend request"
}
```

#### Użytkownik nie znaleziony (404)
```json
{
  "code": 404,
  "message": "User not found"
}
```

#### Próba dodania siebie (400)
```json
{
  "code": 400,
  "message": "Cannot add yourself as a friend"
}
```

#### Już są znajomymi (409)
```json
{
  "code": 409,
  "message": "Accounts are already friends"
}
```

#### Zaproszenie już wysłane (409)
```json
{
  "code": 409,
  "message": "Friend request already sent"
}
```

---

## ACCEPT_FRIEND_REQUEST - Akceptowanie zaproszenia

Akceptowanie zaproszenia do znajomych.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "ACCEPT_FRIEND_REQUEST",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    "requester": "nazwa_uzytkownika_wysylajacego"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `requester` | string | ✅ | Nazwa użytkownika wysyłającego zaproszenie |

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "message": "Friend request accepted"
}
```

#### Zaproszenie nie znalezione (404)
```json
{
  "code": 404,
  "message": "Friend request not found"
}
```

#### Zaproszenie już przetworzone (409)
```json
{
  "code": 409,
  "message": "Friend request already processed"
}
```

---

## REJECT_FRIEND_REQUEST - Odrzucenie zaproszenia

Odrzucenie zaproszenia do znajomych.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "REJECT_FRIEND_REQUEST",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    "requester": "nazwa_uzytkownika_wysylajacego"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `requester` | string | ✅ | Nazwa użytkownika wysyłającego zaproszenie |

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "message": "Friend request rejected"
}
```

#### Zaproszenie nie znalezione (404)
```json
{
  "code": 404,
  "message": "Friend request not found"
}
```

#### Zaproszenie już przetworzone (409)
```json
{
  "code": 409,
  "message": "Friend request already processed"
}
```

---

## GET_FRIENDS - Pobieranie listy znajomych

Pobieranie listy wszystkich znajomych zalogowanego użytkownika.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "GET_FRIENDS",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
  }
}
```

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "message": "Friends retrieved successfully",
  "friends": [
    "jan",
    "anna",
    "piotr"
  ]
}
```

**Uwaga:** Lista zawiera nazwy użytkowników (usernames), nie UUID.

---

## GET_PENDING_REQUESTS - Pobieranie oczekujących zaproszeń

Pobieranie listy wszystkich oczekujących zaproszeń do znajomych.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "GET_PENDING_REQUESTS",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  "body": {
  }
}
```

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "message": "Pending requests retrieved successfully",
  "pendingRequests": [
    {
      "requester": "jan",
      "addressee": "anna",
      "status": 0
    },
    {
      "requester": "piotr",
      "addressee": "anna",
      "status": 0
    }
  ]
}
```

### Status zaproszeń

| Wartość | Status | Opis |
|---------|--------|------|
| `0` | PENDING | Zaproszenie oczekuje na odpowiedź |
| `1` | ACCEPTED | Zaproszenie zaakceptowane |
| `2` | REJECTED | Zaproszenie odrzucone |

---

## Przykłady użycia

### Scenariusz: Wysłanie i akceptowanie zaproszenia

**Krok 1: Jan wysyła zaproszenie do Anny**
```bash
echo '{"method":"SEND_FRIEND_REQUEST","token":"jan_token","body":{"addresseeUsername":"anna"}}' | nc localhost 8080
```

**Krok 2: Anna sprawdza oczekujące zaproszenia**
```bash
echo '{"method":"GET_PENDING_REQUESTS","token":"anna_token","body":{}}' | nc localhost 8080
```

**Krok 3: Anna akceptuje zaproszenie od Jana**
```bash
echo '{"method":"ACCEPT_FRIEND_REQUEST","token":"anna_token","body":{"requester":"jan"}}' | nc localhost 8080
```

**Krok 4: Jan sprawdza listę znajomych**
```bash
echo '{"method":"GET_FRIENDS","token":"jan_token","body":{}}' | nc localhost 8080
```

---

## Powiadomienia

### FRIEND_REQUEST
Wysyłane automatycznie gdy ktoś wyśle zaproszenie do znajomych.

```json
{
  "type": "FRIEND_REQUEST",
  "from": "nazwa_nadawcy",
  "message": "You have a new friend request"
}
```

- Jeśli odbiorca jest **online**: powiadomienie wysyłane natychmiast
- Jeśli odbiorca jest **offline**: powiadomienie zapisywane w kolejce i wysyłane przy następnym logowaniu

---

## Błędy wspólne

#### Nieprawidłowy token (401)
```json
{
  "code": 401,
  "message": "Invalid or expired token"
}
```

#### Brakujące pole (400)
```json
{
  "code": 400,
  "message": "Missing required field: nazwa_pola"
}
```

#### Błąd wewnętrzny (500)
```json
{
  "code": 500,
  "message": "Internal server error"
}
```

