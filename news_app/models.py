from django.contrib.auth.models import User
from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    summary = models.CharField(max_length=300, blank=True, verbose_name='Краткое описание')
    content = models.TextField(verbose_name='Текст новости')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Автор',
    )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
