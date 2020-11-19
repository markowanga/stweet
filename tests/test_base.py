import os.path
from datetime import datetime

import stweet as st


def test_base():
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=phrase,
        from_username=None,
        to_username=None,
        since=datetime(2020, 11, 18),
        until=None,
        language=st.Language.POLISH
    )
    file_path = '{}.csv'.format(phrase).replace('#', 'hashtag_')
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[
            st.PrintFirstInRequestTweetOutput(),
            st.CsvTweetOutput(file_path)
        ]
    ).run()
    assert os.path.isfile(file_path)
