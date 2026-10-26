"""
Пример использования NewsAPIClient.

Запуск (локально, сервер должен быть запущен на порту 8000):
    python -m api_client.example
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client.client import NewsAPIClient

BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:8000')


def main():
    client = NewsAPIClient(BASE_URL)

    print('=== Регистрация пользователя ===')
    user = client.register(
        username='testuser_api',
        email='testuser_api@example.com',
        password='securepass123',
    )
    print(user)

    print('\n=== Вход (получение токена) ===')
    token_data = client.login('testuser_api', 'securepass123')
    print(token_data)

    print('\n=== Создание новости ===')
    news = client.create_news(
        title='Тестовая новость через API',
        summary='Краткое описание тестовой новости',
        content='Это полный текст тестовой новости, созданной через API-клиент. '
                'Длина текста превышает пятьдесят символов для прохождения валидации.',
    )
    print(news)

    news_id = news.get('id')
    if not news_id:
        print('Не удалось создать новость, дальнейшие шаги пропущены.')
        return

    print('\n=== Получение списка новостей ===')
    news_list = client.get_news()
    print(news_list)

    print('\n=== Фильтрация по автору ===')
    author_id = news.get('author')
    if author_id:
        filtered = client.get_news(params={'author': author_id})
        print(filtered)

    print('\n=== Обновление новости ===')
    updated = client.update_news(news_id, title='Обновлённый заголовок')
    print(updated)

    print('\n=== Удаление новости ===')
    status = client.delete_news(news_id)
    print(f'HTTP status: {status}')


if __name__ == '__main__':
    main()
