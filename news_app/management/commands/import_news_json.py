import json
from datetime import datetime
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from news_app.models import News


class Command(BaseCommand):
    help = 'Импорт новостей из news_app/data/news.json в базу данных'

    def handle(self, *args, **options):
        data_file = Path(__file__).resolve().parents[2] / 'data' / 'news.json'
        if not data_file.exists():
            self.stdout.write(self.style.WARNING(f'Файл не найден: {data_file}'))
            return

        with data_file.open('r', encoding='utf-8') as file:
            items = json.load(file)

        if not isinstance(items, list):
            self.stdout.write(self.style.ERROR('JSON должен содержать список новостей'))
            return

        author, _ = User.objects.get_or_create(
            username='web_editor',
            defaults={'email': 'web_editor@localhost'},
        )

        imported = 0
        for item in items:
            title = item.get('title', '').strip()
            content = item.get('content', '').strip()
            if not title or not content:
                continue

            if len(content) < 50:
                content = content.ljust(50, '.')

            news = News.objects.create(
                title=title,
                summary=item.get('summary', ''),
                content=content,
                author=author,
            )

            date_value = item.get('date')
            if date_value:
                try:
                    published = datetime.fromisoformat(date_value).date()
                    aware_dt = timezone.make_aware(
                        datetime.combine(published, datetime.min.time()),
                        timezone.get_current_timezone(),
                    )
                    News.objects.filter(pk=news.pk).update(date_created=aware_dt)
                except (TypeError, ValueError):
                    pass

            imported += 1

        self.stdout.write(self.style.SUCCESS(f'Импортировано новостей: {imported}'))
