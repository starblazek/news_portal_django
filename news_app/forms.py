from django import forms
from django.utils import timezone


class NewsForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label="Заголовок",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите заголовок"}),
    )
    summary = forms.CharField(
        max_length=200,
        label="Краткое описание",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3, "placeholder": "Коротко опишите новость"}
        ),
    )
    content = forms.CharField(
        label="Текст новости",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 8, "placeholder": "Полный текст новости"}
        ),
    )
    date = forms.DateField(
        label="Дата публикации",
        required=False,
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    def clean_date(self):
        return self.cleaned_data.get("date") or timezone.localdate()
