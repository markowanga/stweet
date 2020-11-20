from datetime import datetime

import stweet as st
import stweet.file_reader.read_from_file
from stweet.model.search_tweets_result import SearchTweetsResult


def test_return_tweets_objects():
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=phrase,
        from_username=None,
        to_username=None,
        since=datetime(2020, 11, 18),
        until=None,
        language=st.Language.POLISH
    )
    result = st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[]
    ).run()
    assert isinstance(result, SearchTweetsResult)
    assert result.downloaded_count == len(result.tweets)
    assert result.downloaded_count > 0
    assert all([phrase in it.full_text for it in result.tweets if phrase in it.full_text]) is True


def test_no_return_tweets():
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=phrase,
        from_username=None,
        to_username=None,
        since=datetime(2020, 11, 18),
        until=None,
        language=st.Language.POLISH
    )
    result = st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[],
        return_scrapped_objects=False
    ).run()
    assert isinstance(result, SearchTweetsResult)
    assert result.tweets is None


def test_csv_serialization():
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=phrase,
        from_username=None,
        to_username=None,
        since=datetime(2020, 11, 18),
        until=None,
        language=st.Language.POLISH
    )
    file_name = 'text_file.csv'
    result = st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[
            st.CsvTweetOutput(file_name)
        ],
        return_scrapped_objects=True
    ).run()
    tweets_from_csv = st.file_reader.read_from_file.read_from_csv(file_name)
    assert tweets_from_csv[0] == result.tweets[0]
