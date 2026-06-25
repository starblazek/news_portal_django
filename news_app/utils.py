import json
from datetime import date
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "news.json"


def ensure_data_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        save_news([])


def load_news():
    ensure_data_file()
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []

    if not isinstance(data, list):
        return []
    return data


def save_news(news_list):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)


def generate_next_id(news_list):
    return max((int(news.get("id", 0)) for news in news_list), default=0) + 1


def parse_news_date(news_item):
    value = news_item.get("date")
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def normalize_news_item(news_item):
    normalized = dict(news_item)
    normalized["date_obj"] = parse_news_date(news_item)
    return normalized


def sort_news(news_list):
    return sorted(
        (normalize_news_item(news) for news in news_list),
        key=lambda item: (
            item["date_obj"] or date.min,
            int(item.get("id", 0)),
        ),
        reverse=True,
    )


def get_news_by_id(news_list, news_id):
    for item in news_list:
        if int(item.get("id", 0)) == int(news_id):
            return normalize_news_item(item)
    return None
