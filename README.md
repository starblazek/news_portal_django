# News Portal — Django

Новостной портал с веб-интерфейсом (Часть 1) и REST API (Часть 2/3).

## Возможности

- Веб-сайт: просмотр и добавление новостей (база данных)
- REST API: CRUD для пользователей и новостей (PostgreSQL/SQLite)
- Token- и Session-аутентификация
- Фильтрация новостей по автору, пагинация, валидация
- Клиентский модуль `api_client/` для тестирования API

## Быстрый старт (локально)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

- Веб-сайт: http://127.0.0.1:8000/
- API: http://127.0.0.1:8000/api/
- Документация API: [docs/API.md](docs/API.md)

### Тест API-клиентом

```bash
python -m api_client.example
```

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `SECRET_KEY` | Секретный ключ Django | dev-ключ (только для разработки) |
| `DEBUG` | Режим отладки (`True`/`False`) | `True` |
| `ALLOWED_HOSTS` | Разрешённые хосты через запятую | `localhost,127.0.0.1` |
| `DATABASE_URL` | URL базы данных (PostgreSQL на Render) | SQLite |

## Деплой на Render.com

1. Запушьте репозиторий на GitHub.
2. **New Web Service** → подключите репозиторий.
3. Настройки:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn news_portal.wsgi:application --log-file -`
4. Добавьте переменные окружения:
   - `SECRET_KEY` — случайная строка
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app.onrender.com`
   - `DATABASE_URL` — создаётся автоматически при подключении PostgreSQL
5. Перед первым запуском выполните миграции (Render Shell или добавьте в Build):
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

Альтернативный старт-скрипт: `bin/start.sh` (collectstatic + migrate + gunicorn).

## Структура проекта

```
news_portal/
├── manage.py
├── requirements.txt
├── Procfile
├── news_portal/          # настройки проекта
├── news_app/             # приложение (модели, API, веб-views)
├── api_client/           # клиент для тестирования API
├── docs/API.md           # документация REST API
└── bin/start.sh          # скрипт запуска для Render
```

## Git: ветки и релизы

```bash
git checkout -b part2
git tag -a v2.0 -m "REST API и деплой"
git push origin part2 --tags
```

## Ссылки для сдачи

- Репозиторий: `https://github.com/ВАШ_НИКНЕЙМ/news-portal-django`
- Приложение: `https://news-portal-ВАШ_НИКНЕЙМ.onrender.com`
- API docs: `https://github.com/ВАШ_НИКНЕЙМ/news-portal-django/blob/main/docs/API.md`
- Client: `https://github.com/ВАШ_НИКНЕЙМ/news-portal-django/tree/main/api_client`
