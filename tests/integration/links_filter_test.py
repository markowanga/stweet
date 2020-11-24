import re
from datetime import datetime
from typing import List

import stweet as st
from tests.test_util import tweet_list_assert_condition


def _extract_links(value: str) -> List[str]:
    return re.findall(r'(https?://\S+)', value) or 'https://' in value or 'http://' in value


def _tweet_contains_link(tweet: st.Tweet) -> bool:
    return len(_extract_links(tweet.full_text)) > 0 or tweet.quoted_status_expand_url is not ''


def test_search_with_links():
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        since=datetime(2020, 5, 1),
        until=datetime(2020, 5, 2),
        link_filter=st.LinkFilter.ONLY_WITH_LINKS
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    tweet_list_assert_condition(tweets_collector.get_scrapped_tweets(), lambda tweet: _tweet_contains_link(tweet))


def test_search_without_links():
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_count=500,
        link_filter=st.LinkFilter.ONLY_WITHOUT_LINKS
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    tweet_list_assert_condition(
        tweets=tweets_collector.get_scrapped_tweets(),
        condition=lambda tweet: not _tweet_contains_link(tweet)
    )
