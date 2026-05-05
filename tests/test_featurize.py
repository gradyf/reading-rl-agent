from datetime import date

from reading_rl.featurize import article_to_action_tuple

def test_happy_path_atlantic_article_5_days_ago():
    article = {
        "topic": "ai",
        "word_count": 2233,
        "source_url": "https://www.theatlantic.com/economy/2026/05/ai-bubble-revenue-anthropic/687022/",
        "added": date(2026,4,1)
    }

    today = date(2026,4,6)

    result = article_to_action_tuple(article,today)

    assert result == ("ai","long","longform-mag","fresh")