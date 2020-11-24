import sys
from io import StringIO

import stweet as st
from tests.test_util import get_tweets_to_tweet_output_test
from tests.tweet_output_counter import TweetOutputCounter


def test_print_all_tweet_output():
    captured_output = StringIO()
    sys.stdout = captured_output
    tweets_collector = st.CollectorTweetOutput()
    get_tweets_to_tweet_output_test([
        st.PrintTweetOutput(),
        tweets_collector
    ])
    sys.stdout = sys.__stdout__
    captured_output.getvalue().count('Tweet(')
    assert captured_output.getvalue().count('Tweet(') == len(tweets_collector.get_scrapped_tweets())


def test_print_batch_single_tweet_tweet_output():
    captured_output = StringIO()
    sys.stdout = captured_output
    tweet_output_counter = TweetOutputCounter()
    get_tweets_to_tweet_output_test([
        st.PrintFirstInRequestTweetOutput(),
        tweet_output_counter
    ])
    sys.stdout = sys.__stdout__
    captured_output.getvalue().count('Tweet(')
    print_tweet_count = captured_output.getvalue().count('Tweet(')
    print_no_tweets_line = captured_output.getvalue().count('PrintFirstInRequestTweetOutput -- no tweets to print')
    assert (print_tweet_count + print_no_tweets_line) == tweet_output_counter.get_output_call_count()
