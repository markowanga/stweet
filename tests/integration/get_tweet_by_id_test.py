import stweet as st


def test_get_tweets_by_ids():
    tweets_ids = ['1337071849772093442', '1337067073051238400']
    task = st.TweetsByIdsTask(tweets_ids)
    collect_output = st.CollectorTweetOutput()
    result = st.TweetsByIdsRunner(task, [collect_output]).run()
    scrapped_tweets_ids = [it.id_str for it in collect_output.get_scrapped_tweets()]
    assert result.downloaded_count == len(tweets_ids)
    assert len(collect_output.get_scrapped_tweets()) == len(tweets_ids)
    assert sorted(scrapped_tweets_ids) == sorted(tweets_ids)
