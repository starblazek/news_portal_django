from django import forms

from .models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'summary', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Коротко опишите новость',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Полный текст новости',
            }),
        }
        labels = {
            'title': 'Заголовок',
            'summary': 'Краткое описание',
            'content': 'Текст новости',
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        if len(content) < 50:
            raise forms.ValidationError('Минимум 50 символов.')
        return content
