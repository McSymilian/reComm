## AUTH - Logowanie użytkownika

Autentykacja istniejącego użytkownika w systemie.

### Wymagana autentykacja
❌ Nie

### Żądanie

```json
{
  "method": "AUTH",
  "body": {
    "password": "haslo",
    "username": "nazwa_uzytkownika"
  }
}
```

### Parametry
| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `password` | string | ✅ | Hasło użytkownika |
| `username` | string | ✅ | Nazwa użytkownika |

### Odpowiedzi

#### Sukces (200)
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Authenticated",
  "code": 200
}
```

**Uwaga:** Token JWT powinien być używany w kolejnych żądaniach wymagających autentykacji.

### Przykłady błędów

#### Nieprawidłowe dane logowania (401)
```json
{
  "message": "Invalid credentials",
  "code": 401
}
```

#### Brakujące pole (400)
```json
{
  "message": "Missing required field: password",
  "code": 400
}
```

lub

```json
{
  "message": "Missing required field: username",
  "code": 400
}
```
### Przykład użycia
**Request:**
```bash
echo '{"method":"AUTH","body":{"username":"jan","password":"haslo123"}}' | nc localhost 8080
```
**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI0MDk2MDAsImlhdCI6MTczMjMyMzIwMCwiaXNzIjoicmVDb21tIiwidXVpZCI6IjEyMzQ1Njc4LTkwYWItY2RlZi0xMjM0LTU2Nzg5MGFiY2RlZiJ9.signature",
  "message": "Authenticated",
  "code": 200
}
```
### Dodatkowe informacje

### Bezpieczeństwo
Po udanym logowaniu:
1. Użytkownik otrzymuje token JWT ważny przez 12 godziny
2. Połączenie TCP pozostaje otwarte
3. Użytkownik jest rejestrowany jako online w `ConnectionManager`
4. Wszystkie zaległe powiadomienia są wysyłane automatycznie
5. Użytkownik będzie otrzymywać powiadomienia w czasie rzeczywistym

# API Autentykacji
- Nieudane próby logowania są logowane
- Token JWT jest podpisany kluczem tajnym serwera
- Hasła są hashowane za pomocą bcrypt przed zapisaniem w bazie danych