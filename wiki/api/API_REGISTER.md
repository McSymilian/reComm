# API Rejestracji

## REGISTER - Rejestracja nowego użytkownika

Utworzenie nowego konta użytkownika w systemie.

### Wymagana autentykacja
❌ Nie

### Żądanie

```json
{
  "method": "REGISTER",
  "body": {
    "username": "nazwa_uzytkownika",
    "password": "haslo"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `username` | string | ✅ | Nazwa użytkownika (unikalna) |
| `password` | string | ✅ | Hasło użytkownika |

### Odpowiedzi

#### Sukces (201)
```json
{
  "code": 201,
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Uwaga:** Token JWT jest automatycznie generowany i zwracany po rejestracji. Użytkownik jest od razu zalogowany.

#### Użytkownik już istnieje (409)
```json
{
  "code": 409,
  "message": "Username is already taken"
}
```

#### Brakujące pole (400)
```json
{
  "code": 400,
  "message": "Missing required field: username"
}
```

lub

```json
{
  "code": 400,
  "message": "Missing required field: password"
}
```

### Przykład użycia

**Request:**
```bash
echo '{"method":"REGISTER","body":{"username":"nowy_user","password":"bezpieczne_haslo"}}' | nc localhost 8080
```

**Response:**
```json
{
  "code": 201,
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI0MDk2MDAsImlhdCI6MTczMjMyMzIwMCwiaXNzIjoicmVDb21tIiwidXVpZCI6ImFiY2RlZjEyLTM0NTYtNzg5MC1hYmNkLWVmMTIzNDU2Nzg5MCJ9.signature"
}
```

### Proces rejestracji

1. System sprawdza czy nazwa użytkownika jest dostępna
2. Hasło jest hashowane za pomocą bcrypt
3. Tworzony jest nowy użytkownik z unikalnym UUID
4. Użytkownik jest zapisywany w bazie danych (plik JSON)
5. Generowany jest token JWT
6. Użytkownik jest automatycznie zalogowany
7. Połączenie TCP pozostaje otwarte
8. Użytkownik jest rejestrowany jako online w `ConnectionManager`

### Dodatkowe informacje

Po udanej rejestracji:
- Token JWT jest ważny przez 12 godziny
- Użytkownik nie musi się dodatkowo logować
- Połączenie pozostaje aktywne do odbierania powiadomień
- UUID użytkownika jest generowane automatycznie
- Data utworzenia konta jest zapisywana