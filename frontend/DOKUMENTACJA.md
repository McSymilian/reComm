# reComm - Dokumentacja Frontendu

## Przegląd Aplikacji

**reComm** to aplikacja do komunikacji w czasie rzeczywistym zbudowana w Pythonie z wykorzystaniem biblioteki CustomTkinter. Aplikacja umożliwia:
- Rejestrację i logowanie użytkowników
- Wysyłanie wiadomości prywatnych
- Tworzenie i zarządzanie grupami
- Obsługę zaproszeń do znajomych
- Odbieranie powiadomień w czasie rzeczywistym

---

## Architektura Systemu

### Struktura Katalogów

```
frontend/
├── main.py                 # Punkt wejścia aplikacji
├── src/
│   ├── app.py              # Główna klasa aplikacji
│   ├── components/         # Komponenty UI
│   │   ├── login_frame.py
│   │   ├── main_screen.py
│   │   ├── conversation_list.py
│   │   ├── conversation_frame.py
│   │   ├── friend_requests_frame.py
│   │   ├── group_actions_dialog.py
│   │   └── ...
│   ├── utils/              # Narzędzia
│   │   ├── api_client.py   # Komunikacja z serwerem
│   │   ├── connection.py   # Połączenie WebSocket
│   │   └── data_store.py   # Zarządzanie stanem
│   └── pydantic_classes/   # Modele danych
```

### Warstwy Aplikacji

```
┌─────────────────────────────────────┐
│         Warstwa UI (CustomTkinter)  │  ← Komponenty wizualne
├─────────────────────────────────────┤
│         DataStore (Stan aplikacji)  │  ← Centralne zarządzanie danymi
├─────────────────────────────────────┤
│         APIClient (Logika biznesowa)│  ← Obsługa żądań/odpowiedzi
├─────────────────────────────────────┤
│         Connection (WebSocket)      │  ← Komunikacja sieciowa
└─────────────────────────────────────┘
```

---

## Kluczowe Komponenty

### 1. APIClient - Komunikacja z Serwerem

`APIClient` odpowiada za całą komunikację z backendem poprzez WebSocket. Obsługuje wysyłanie żądań i odbieranie odpowiedzi oraz powiadomień.

```python
class APIClient:
    def __init__(self, host: str, port: int):
        self.connection = Connection(host, port)
        self._resp_queue = Queue()
        self._notification_callback = None
        
    def _send_request(self, request: BaseRequest, timeout=10) -> dict:
        request_dict = request.model_dump()
        request_dict["token"] = self.token
        self.connection.send(json.dumps(request_dict))
        response_dict = self._resp_queue.get(timeout=timeout)
        return response_dict
```

### 2. DataStore - Zarządzanie Stanem

`DataStore` przechowuje cały stan aplikacji i powiadamia komponenty UI o zmianach poprzez system callbacków.

```python
class DataStore:
    def __init__(self, client):
        self.client: APIClient = client
        self.conversations: Dict[str, List[MessageModel]] = {}
        self.friends: List[str] = []
        self.groups: List[Group] = []
        self._ui_callbacks: dict[str, list[callable]] = {}
    
    def _notify_ui(self, event_type: str, data=None):
        for callback in self._ui_callbacks.get(event_type, []):
            callback(data)
```

### 3. Reaktywne Aktualizacje UI

Komponenty rejestrują się na zdarzenia w DataStore i automatycznie aktualizują UI:

```python
class ConversationList(ctk.CTkScrollableFrame):
    def __init__(self, master, data_store, api_client, on_select_conversation):
        self.data_store.register_ui_callback("friends_updated", self._on_data_updated)
        self.data_store.register_ui_callback("groups_updated", self._on_data_updated)
    
    def _on_data_updated(self, data=None):
        self.after(0, self.refresh)
```

---

## Przepływ Danych

### Wysyłanie Wiadomości

```
1. Użytkownik klika "Wyślij"
       ↓
2. ConversationFrame._send_message()
       ↓
3. APIClient.send_private_message()
       ↓
4. Connection wysyła przez WebSocket
       ↓
5. Serwer odpowiada (code: 200)
       ↓
6. DataStore.add_message_to_conversation()
       ↓
7. UI automatycznie się odświeża
```

### Odbieranie Powiadomień

```
1. Serwer wysyła powiadomienie (WebSocket)
       ↓
2. Connection._receive_loop() odbiera dane
       ↓
3. APIClient rozpoznaje typ powiadomienia
       ↓
4. DataStore.process_notification()
       ↓
5. DataStore powiadamia UI przez callbacki
       ↓
6. Komponenty automatycznie się odświeżają
```

---

## Modele Danych (Pydantic)

Aplikacja używa Pydantic do walidacji danych:

```python
class MessageModel(BaseModel):
    messageId: str
    senderName: str
    content: str
    sentAt: int
    type: MessageType
```

---

## Uruchomienie Aplikacji

```bash
cd frontend
uv run main.py
```

Aplikacja łączy się z serwerem pod podanymi parametrami i wyświetla ekran logowania.

---

## Podsumowanie

reComm wykorzystuje architekturę warstwową z:
- **Reaktywnym UI** - komponenty automatycznie reagują na zmiany stanu
- **Centralnym DataStore** - jedno źródło prawdy dla całej aplikacji  
- **WebSocket** - komunikacja w czasie rzeczywistym
- **Pydantic** - typowanie i walidacja danych
