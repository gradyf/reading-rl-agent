from datetime import date
from urllib.parse import urlsplit

def category_bucket(article):
    if article["topic"] == "ai":
        return "ai"
    else: 
        return "other"

def length_bucket(article):
    if article["word_count"] <= 750:
        return "short"
    elif article["word_count"] <= 1500:
        return "medium"
    else:
        return "long"


def source_category(article):
    article_url = urlsplit(article["source_url"])
    hostname = article_url.hostname
    if "theatlantic" in hostname:
        return "longform-mag"
    return None

def recency_bucket(article, today: date):
    date_diff = (today - article["added"]).days

    if date_diff <= 7:
        return "fresh"
    elif date_diff <= 30:
        return "aged"
    else:
        return "stale"

def article_to_action_tuple(article,today):
    category = category_bucket(article)
    length = length_bucket(article)
    source = source_category(article)
    recency = recency_bucket(article, today)

    return (category, length, source, recency)


