from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import NewsForm
from .models import News


def get_web_author():
    user, _ = User.objects.get_or_create(
        username='web_editor',
        defaults={'email': 'web_editor@localhost'},
    )
    return user


def home_view(request):
    news_list = News.objects.select_related('author').all()
    today = timezone.localdate()

    return render(request, 'home.html', {
        'news_list': news_list,
        'today': today,
    })


def news_detail_view(request, news_id):
    news_item = get_object_or_404(News.objects.select_related('author'), pk=news_id)

    return render(request, 'news_detail.html', {
        'news': news_item,
    })


def add_news_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            author = request.user if request.user.is_authenticated else get_web_author()
            form.save(commit=False)
            form.instance.author = author
            form.save()
            return redirect('success')
    else:
        form = NewsForm()

    return render(request, 'add_news.html', {
        'form': form,
    })


def success_view(request):
    return render(request, 'success.html')


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
