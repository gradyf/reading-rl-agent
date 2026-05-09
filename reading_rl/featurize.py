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


def budget_bucket(remaining_min):
    if remaining_min <= 10:
        return "short"
    elif remaining_min <= 25:
        return "med"
    else:
        return "long"

def last_topic_tagger(last_topic):
    return last_topic

def articles_read_counter(articles_read):
    if articles_read > 3:
        return 3
    else:
        return articles_read



def article_to_action_tuple(article,today):
    category = category_bucket(article)
    length = length_bucket(article)
    source = source_category(article)
    recency = recency_bucket(article, today)

    return (category, length, source, recency)



def state_to_tuple(remaining_min, last_topic, articles_read):
    budget = budget_bucket(remaining_min)
    last_topic_tag = last_topic_tagger(last_topic)
    articles_read_count = articles_read_counter(articles_read);

    return (budget, last_topic_tag, articles_read_count)



