# REST API — News Portal

Базовый URL: `/api/`

Аутентификация: **Token** (`Authorization: Token <token>`) или **Session** (cookie после входа в браузере).

Получение токена:

```http
POST /api/token/
Content-Type: application/json

{
  "username": "user",
  "password": "password"
}
```

Ответ:

```json
{"token": "9944b09199c62bcf9418ad846dd0e4bbdfc882ee"}
```

---

## Пользователи

| Метод | URL | Описание | Аутентификация |
|-------|-----|----------|----------------|
| GET | `/api/users/` | Список пользователей | Не обязательна (чтение) |
| POST | `/api/users/` | Регистрация | Не требуется |
| GET | `/api/users/<id>/` | Детали пользователя | Не обязательна (чтение) |
| PUT/PATCH | `/api/users/<id>/` | Обновление | Требуется (свой аккаунт) |
| DELETE | `/api/users/<id>/` | Удаление | Требуется (свой аккаунт) |

### Регистрация

```http
POST /api/users/
Content-Type: application/json

{
  "username": "ivan",
  "email": "ivan@example.com",
  "password": "securepass123"
}
```

---

## Новости

| Метод | URL | Описание | Аутентификация |
|-------|-----|----------|----------------|
| GET | `/api/news/` | Список новостей | Не обязательна |
| POST | `/api/news/` | Создание | Требуется |
| GET | `/api/news/<id>/` | Детали | Не обязательна |
| PUT/PATCH | `/api/news/<id>/` | Обновление | Требуется (автор) |
| DELETE | `/api/news/<id>/` | Удаление | Требуется (автор) |

### Создание новости

```http
POST /api/news/
Authorization: Token <token>
Content-Type: application/json

{
  "title": "Заголовок",
  "summary": "Краткое описание",
  "content": "Полный текст новости, не менее 50 символов для прохождения валидации."
}
```

Поле `author` устанавливается автоматически из текущего пользователя.

### Фильтрация

```http
GET /api/news/?author=5
```

Возвращает новости пользователя с `id=5`.

### Пагинация

Списки пагинируются по **10** записей на страницу (по умолчанию):

```json
{
  "count": 25,
  "next": "http://example.com/api/news/?page=2",
  "previous": null,
  "results": [...]
}
```

### Валидация (ошибки 400)

```json
{
  "title": ["Это поле обязательно."],
  "content": ["Минимум 50 символов."]
}
```

### Права доступа

- **Чтение** (`GET`) — доступно всем.
- **Создание** (`POST`) — только аутентифицированным пользователям.
- **Изменение/удаление** — только автор новости.

---

## Пример с curl

```bash
# Регистрация
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"demo12345"}'

# Получение токена
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo12345"}'

# Создание новости
curl -X POST http://127.0.0.1:8000/api/news/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"This is a news article with more than fifty characters in total."}'
```

---

## Клиентский модуль

См. каталог [`api_client/`](../api_client/) и скрипт [`api_client/example.py`](../api_client/example.py).

```bash
python -m api_client.example
```
