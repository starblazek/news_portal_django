import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from . import utils


class NewsPortalTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "news.json"

        self.data_dir_patch = patch.object(utils, "DATA_DIR", Path(self.temp_dir.name))
        self.data_file_patch = patch.object(utils, "DATA_FILE", self.data_file)
        self.data_dir_patch.start()
        self.data_file_patch.start()

    def tearDown(self):
        self.data_file_patch.stop()
        self.data_dir_patch.stop()
        self.temp_dir.cleanup()

    def test_home_page_shows_empty_state(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Новостей пока нет")

    def test_add_news_saves_to_json_and_redirects_to_success(self):
        response = self.client.post(
            reverse("add_news"),
            {
                "title": "Тестовая новость",
                "summary": "Краткое описание",
                "content": "Полный текст новости",
                "date": "2026-06-25",
            },
        )

        self.assertRedirects(response, reverse("success"))

        saved_news = utils.load_news()
        self.assertEqual(len(saved_news), 1)
        self.assertEqual(saved_news[0]["id"], 1)
        self.assertEqual(saved_news[0]["title"], "Тестовая новость")

    def test_detail_page_returns_404_for_missing_news(self):
        response = self.client.get(reverse("news_detail", args=[999]))

        self.assertEqual(response.status_code, 404)
