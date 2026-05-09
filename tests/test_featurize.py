import pytest
from datetime import date
import reading_rl.featurize as feat


def test_happy_path_atlantic_article_5_days_ago():
    article = {
        "topic": "ai",
        "word_count": 2233,
        "source_url": "https://www.theatlantic.com/economy/2026/05/ai-bubble-revenue-anthropic/687022/",
        "added": date(2026,4,1)
    }

    today = date(2026,4,6)

    result = feat.article_to_action_tuple(article,today)

    assert result == ("ai","long","longform-mag","fresh")

@pytest.mark.parametrize("word_count, expected", [
    (1, "short"),
    (500, "short"),
    (749, "short"),
    (750, "short"),
    (751, "medium"),
    (1500, "medium"),
    (1501, "long"),
    (99999, "long")
])
def test_length_bucket_threshold(word_count, expected):
    assert feat.length_bucket({"word_count": word_count}) == expected


@pytest.mark.parametrize("added_date, today, expected", [
    (date(2026,4,1),date(2026,4,7),"fresh"),
    (date(2026,4,1),date(2026,4,8),"fresh"),
    (date(2026,4,1),date(2026,4,9),"aged"),
    (date(2026,4,1),date(2026,4,15),"aged"),
    (date(2026,4,1),date(2026,4,30),"aged"),
    (date(2026,4,1),date(2026,5,1),"aged"),
    (date(2026,4,1),date(2026,5,2),"stale"),
])
def test_recency_bucket(added_date, today, expected):
    assert feat.recency_bucket({"added":added_date},today) == expected


def test_happy_path_state_tuple():

    remaining_min = 15
    last_topic = None
    articles_read = 15

    result = feat.state_to_tuple(remaining_min, last_topic, articles_read)

    assert result == ("med",None,3)

@pytest.mark.parametrize("remaining_min, expected", [
    (1,"short"),
    (9,"short"),
    (10,"short"),
    (11,"med"),
    (15,"med"),
    (24,"med"),
    (25,"med"),
    (26,"long"),
    (9999,"long")
])
def test_remaining_min_bucket(remaining_min,expected):
    assert feat.budget_bucket(remaining_min) == expected

@pytest.mark.parametrize("articles_read, expected", [
    (0,0),
    (1,1),
    (2,2),
    (3,3),
    (4,3),
    (9999,3)
])
def test_articles_read_counter(articles_read,expected):
    assert feat.articles_read_counter(articles_read) == expected