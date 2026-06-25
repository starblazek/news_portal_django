from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import NewsForm
from .utils import (
    generate_next_id,
    get_news_by_id,
    load_news,
    save_news,
    sort_news,
)

def home_view(request):
    news_list = sort_news(load_news())
    today = timezone.localdate()

    for item in news_list:
        item["date_display"] = item["date_obj"].strftime("%d.%m.%Y") if item["date_obj"] else "Без даты"
        item["is_today"] = item["date_obj"] == today

    return render(request, "home.html", {
        "news_list": news_list,
    })


def news_detail_view(request, news_id):
    news_item = get_news_by_id(load_news(), news_id)
    if not news_item:
        raise Http404("Новость не найдена")

    news_item["date_display"] = news_item["date_obj"].strftime("%d.%m.%Y") if news_item["date_obj"] else "Без даты"

    return render(request, "news_detail.html", {
        "news": news_item,
    })


def add_news_view(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news_list = load_news()
            published_date = form.cleaned_data["date"]
            news_list.append(
                {
                    "id": generate_next_id(news_list),
                    "title": form.cleaned_data["title"],
                    "summary": form.cleaned_data["summary"],
                    "content": form.cleaned_data["content"],
                    "date": published_date.isoformat(),
                }
            )
            save_news(news_list)
            return redirect("success")
    else:
        form = NewsForm()

    return render(request, "add_news.html", {
        "form": form,
    })


def success_view(request):
    return render(request, "success.html")


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)
