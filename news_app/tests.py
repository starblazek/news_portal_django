from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import News


class NewsPortalTests(TestCase):
    def test_home_page_shows_empty_state(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новостей пока нет')

    def test_add_news_saves_to_database_and_redirects_to_success(self):
        response = self.client.post(
            reverse('add_news'),
            {
                'title': 'Тестовая новость',
                'summary': 'Краткое описание',
                'content': 'Полный текст новости для проверки сохранения в базе данных.',
            },
        )

        self.assertRedirects(response, reverse('success'))
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(News.objects.first().title, 'Тестовая новость')

    def test_detail_page_returns_404_for_missing_news(self):
        response = self.client.get(reverse('news_detail', args=[999]))

        self.assertEqual(response.status_code, 404)

    def test_home_page_shows_news_from_database(self):
        author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='password123',
        )
        News.objects.create(
            title='Опубликованная новость',
            summary='Кратко',
            content='Длинный текст новости для отображения на главной странице сайта.',
            author=author,
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Опубликованная новость')
