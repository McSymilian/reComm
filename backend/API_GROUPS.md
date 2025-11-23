# API Grup

## Przegląd

System grup umożliwia użytkownikom tworzenie grup, dodawanie swoich znajomych do grup, zarządzanie nimi oraz ich opuszczanie.

**Ważne zasady:**
- Tylko znajomi mogą być dodawani do grup
- Każdy członek grupy może dodawać swoich znajomych
- Każdy członek może zmienić nazwę grupy
- Każdy członek może opuścić grupę
- Tylko twórca grupy może ją usunąć
- Ostatni członek nie może opuścić grupy (musi ją usunąć)

---

## CREATE_GROUP - Utworzenie grupy

Utworzenie nowej grupy. Twórca automatycznie staje się pierwszym członkiem.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "CREATE_GROUP",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    "groupName": "Nazwa grupy"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `groupName` | string | ✅ | Nazwa grupy |

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "message": "Group created successfully",
  "groupId": "12345678-90ab-cdef-1234-567890abcdef"
}
```

#### Brakujące pole (400)
```json
{
  "code": 400,
  "message": "Missing required field: groupName"
}
```

---

## ADD_MEMBER_TO_GROUP - Dodanie członka do grupy

Dodanie znajomego do grupy. Tylko członkowie grupy mogą dodawać nowych członków, a dodawany użytkownik musi być znajomym osoby dodającej.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "ADD_MEMBER_TO_GROUP",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    "groupId": "12345678-90ab-cdef-1234-567890abcdef",
    "username": "nazwa_uzytkownika"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `groupId` | string | ✅ | UUID grupy |
| `username` | string | ✅ | Nazwa użytkownika do dodania |

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "message": "Member added to group successfully"
}
```

#### Grupa nie znaleziona (404)
```json
{
  "code": 404,
  "message": "Group not found"
}
```

#### Użytkownik nie znaleziony (404)
```json
{
  "code": 404,
  "message": "User not found"
}
```

#### Nie jesteś członkiem grupy (403)
```json
{
  "code": 403,
  "message": "You are not a member of this group"
}
```

#### Użytkownik nie jest znajomym (400)
```json
{
  "code": 400,
  "message": "Cannot add non-friend to group"
}
```

#### Użytkownik już w grupie (409)
```json
{
  "code": 409,
  "message": "User is already in the group"
}
```

#### Nieprawidłowe ID grupy (400)
```json
{
  "code": 400,
  "message": "Invalid group ID"
}
```

---

## UPDATE_GROUP_NAME - Zmiana nazwy grupy

Zmiana nazwy grupy. Każdy członek grupy może zmienić nazwę.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "UPDATE_GROUP_NAME",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    "groupId": "12345678-90ab-cdef-1234-567890abcdef",
    "newName": "Nowa nazwa grupy"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `groupId` | string | ✅ | UUID grupy |
| `newName` | string | ✅ | Nowa nazwa grupy |

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "message": "Group name updated successfully"
}
```

#### Grupa nie znaleziona (404)
```json
{
  "code": 404,
  "message": "Group not found"
}
```

#### Nie jesteś członkiem grupy (403)
```json
{
  "code": 403,
  "message": "You are not a member of this group"
}
```

---

## LEAVE_GROUP - Opuszczenie grupy

Opuszczenie grupy przez członka. Ostatni członek nie może opuścić grupy - musi ją usunąć.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "LEAVE_GROUP",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    "groupId": "12345678-90ab-cdef-1234-567890abcdef"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `groupId` | string | ✅ | UUID grupy |

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "message": "Left group successfully"
}
```

#### Grupa nie znaleziona (404)
```json
{
  "code": 404,
  "message": "Group not found"
}
```

#### Nie jesteś członkiem grupy (403)
```json
{
  "code": 403,
  "message": "You are not a member of this group"
}
```

#### Ostatni członek nie może opuścić (400)
```json
{
  "code": 400,
  "message": "Cannot leave group as the last member. Delete the group instead."
}
```

---

## DELETE_GROUP - Usunięcie grupy

Całkowite usunięcie grupy.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "DELETE_GROUP",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    "groupId": "12345678-90ab-cdef-1234-567890abcdef"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `groupId` | string | ✅ | UUID grupy |

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "message": "Group deleted successfully"
}
```

#### Grupa nie znaleziona (404)
```json
{
  "code": 404,
  "message": "Group not found"
}
```

#### Brak uprawnień (403)
```json
{
  "code": 403,
  "message": "Only the group creator can delete the group"
}
```

---

## GET_USER_GROUPS - Pobieranie grup użytkownika

Pobieranie listy wszystkich grup, do których należy użytkownik.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "GET_USER_GROUPS",
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
  "groups": [
    {
      "id": "12345678-90ab-cdef-1234-567890abcdef",
      "name": "Przyjaciele",
      "creatorId": "abcdef12-3456-7890-abcd-ef1234567890",
      "memberIds": [
        "abcdef12-3456-7890-abcd-ef1234567890",
        "fedcba98-7654-3210-fedc-ba9876543210"
      ],
      "createdAt": "2025-01-15T10:30:00Z"
    },
    {
      "id": "87654321-ba09-fedc-4321-0987654321fe",
      "name": "Projekt",
      "creatorId": "fedcba98-7654-3210-fedc-ba9876543210",
      "memberIds": [
        "abcdef12-3456-7890-abcd-ef1234567890",
        "fedcba98-7654-3210-fedc-ba9876543210",
        "11111111-2222-3333-4444-555555555555"
      ],
      "createdAt": "2025-01-16T14:20:00Z"
    }
  ]
}
```

---

## GET_GROUP_DETAILS - Pobieranie szczegółów grupy

Pobieranie szczegółowych informacji o konkretnej grupie. Tylko członkowie grupy mogą przeglądać jej szczegóły.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "GET_GROUP_DETAILS",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    "groupId": "12345678-90ab-cdef-1234-567890abcdef"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `groupId` | string | ✅ | UUID grupy |

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "group": {
    "id": "12345678-90ab-cdef-1234-567890abcdef",
    "name": "Przyjaciele",
    "creatorId": "abcdef12-3456-7890-abcd-ef1234567890",
    "memberIds": [
      "abcdef12-3456-7890-abcd-ef1234567890",
      "fedcba98-7654-3210-fedc-ba9876543210"
    ],
    "createdAt": "2025-01-15T10:30:00Z"
  }
}
```

#### Grupa nie znaleziona (404)
```json
{
  "code": 404,
  "message": "Group not found"
}
```

#### Nie jesteś członkiem grupy (403)
```json
{
  "code": 403,
  "message": "You are not a member of this group"
}
```

---

## GET_GROUP_MEMBERS - Pobieranie członków grupy

Pobieranie listy członków grupy z ich nazwami użytkowników. Tylko członkowie grupy mogą zobaczyć listę.

### Wymagana autentykacja
✅ Tak (token JWT)

### Żądanie

```json
{
  "method": "GET_GROUP_MEMBERS",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "body": {
    "groupId": "12345678-90ab-cdef-1234-567890abcdef"
  }
}
```

### Parametry

| Parametr | Typ | Wymagany | Opis |
|----------|-----|----------|------|
| `groupId` | string | ✅ | UUID grupy |

### Odpowiedzi

#### Sukces (200)
```json
{
  "code": 200,
  "members": [
    {
      "uuid": "abcdef12-3456-7890-abcd-ef1234567890",
      "username": "jan"
    },
    {
      "uuid": "fedcba98-7654-3210-fedc-ba9876543210",
      "username": "anna"
    }
  ]
}
```

#### Grupa nie znaleziona (404)
```json
{
  "code": 404,
  "message": "Group not found"
}
```

#### Nie jesteś członkiem grupy (403)
```json
{
  "code": 403,
  "message": "You are not a member of this group"
}
```

---

## Przykłady użycia

### Scenariusz: Tworzenie grupy i dodawanie członków

**Krok 1: Jan tworzy grupę**
```bash
echo '{"method":"CREATE_GROUP","token":"jan_token","body":{"groupName":"Projekt XYZ"}}' | nc localhost 8080
```

Response:
```json
{
  "code": 200,
  "message": "Group created successfully",
  "groupId": "12345678-90ab-cdef-1234-567890abcdef"
}
```

**Krok 2: Jan dodaje swojego znajomego Annę do grupy**
```bash
echo '{"method":"ADD_MEMBER_TO_GROUP","token":"jan_token","body":{"groupId":"12345678-90ab-cdef-1234-567890abcdef","username":"anna"}}' | nc localhost 8080
```

**Krok 3: Anna dodaje swojego znajomego Piotra**
```bash
echo '{"method":"ADD_MEMBER_TO_GROUP","token":"anna_token","body":{"groupId":"12345678-90ab-cdef-1234-567890abcdef","username":"piotr"}}' | nc localhost 8080
```

**Krok 4: Piotr zmienia nazwę grupy**
```bash
echo '{"method":"UPDATE_GROUP_NAME","token":"piotr_token","body":{"groupId":"12345678-90ab-cdef-1234-567890abcdef","newName":"Super Projekt"}}' | nc localhost 8080
```

**Krok 5: Sprawdzenie członków grupy**
```bash
echo '{"method":"GET_GROUP_MEMBERS","token":"jan_token","body":{"groupId":"12345678-90ab-cdef-1234-567890abcdef"}}' | nc localhost 8080
```

**Krok 6: Piotr opuszcza grupę**
```bash
echo '{"method":"LEAVE_GROUP","token":"piotr_token","body":{"groupId":"12345678-90ab-cdef-1234-567890abcdef"}}' | nc localhost 8080
```

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

#### Nieprawidłowy format UUID (400)
```json
{
  "code": 400,
  "message": "Invalid group ID"
}
```

#### Błąd wewnętrzny (500)
```json
{
  "code": 500,
  "message": "Internal server error"
}
```

---

## Model danych grupy

```json
{
  "id": "UUID",
  "name": "string",
  "creatorId": "UUID",
  "memberIds": ["UUID", "UUID", ...],
  "createdAt": "ISO 8601 timestamp"
}
```

### Pola

| Pole | Typ | Opis |
|------|-----|------|
| `id` | UUID string | Unikalny identyfikator grupy |
| `name` | string | Nazwa grupy |
| `creatorId` | UUID string | UUID twórcy grupy |
| `memberIds` | array of UUID strings | Lista UUID członków |
| `createdAt` | ISO 8601 string | Data utworzenia grupy |

