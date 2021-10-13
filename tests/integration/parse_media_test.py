import stweet as st


def test_scrap_tweet_with_single_media():
    tweets_ids = ['1357358278746005508']
    collector = st.CollectorTweetOutput()
    st.TweetsByIdRunner(st.TweetsByIdTask(tweets_ids), [collector]).run()
    tweets = collector.get_raw_list()
    assert len(tweets) == 1
    assert len(tweets[0].media) == 1


def test_scrap_tweet_with_double_media():
    tweets_ids = ['1115978039534297088']
    collector = st.CollectorTweetOutput()
    st.TweetsByIdRunner(st.TweetsByIdTask(tweets_ids), [collector]).run()
    tweets = collector.get_raw_list()
    assert len(tweets) == 1
    assert len(tweets[0].media) == 2
