Scrap tweets by ids
===================

.. code:: python

    import stweet as st

Prepare task
------------

Task named ``TweetsByIdsRunner`` has only one property, which define
tweet ids – ``tweet_ids: List[str]``.

.. code:: python

    task = st.TweetsByIdsTask(['1357358278746005508', '1115978039534297088', '56546745646545646574'])

Prepate TweetOutputs
--------------------

Tweet output collect the result of scrapped tweets.

.. code:: python

    tweet_outputs = [st.PrintTweetOutput()]

Example task execution
----------------------

``TweetsByIdsRunner`` scrap tweets by id. Runner needs always
``tweets_by_ids_task`` and ``tweet_outputs``. This is all properties of
``TweetsByIdsRunner``: - **``tweets_by_ids_task: TweetsByIdsTask``** –
task with tweets to scrap definition -
**``tweet_outputs: List[TweetOutput]``** – objects to export scrapped
tweets -
**``tweets_by_ids_context: Optional[TweetsByIdsContext] = None``** –
context of scrapping, it can continoue the paused scrapping or put
initial auth token, if None the basic context is provided -
**``web_client: WebClient = RequestsWebClient()``** – client to execute
web connections, here can be configure proxy connection for example -
**``tweet_parser: TweetParser = BaseTweetParser()``** – parser of tweet
response from Twitter -
**``auth_token_provider_factory: AuthTokenProviderFactory = SimpleAuthTokenProviderFactory()``**
– provider of auth token

.. code:: python

    run_result = st.TweetsByIdsRunner(task, tweet_outputs).run()


.. parsed-literal::

    Tweet(created_at=<Arrow [2021-02-04T16:00:06+00:00]>, id_str='1357358278746005508', conversation_id_str='1357358278746005508', full_text='Extending the moratorium on evictions and foreclosures to help countless Americans keep a roof over their head — that’s the American Rescue Plan. https://t.co/Xbviqqr47w', lang='en', favorited=False, retweeted=False, retweet_count=6300, favorite_count=43573, reply_count=3366, quote_count=366, quoted_status_id_str='', quoted_status_short_url='', quoted_status_expand_url='', user_id_str='1349149096909668363', user_name='POTUS', user_full_name='President Biden', user_verified=True, in_reply_to_status_id_str='', in_reply_to_user_id_str='', media=[Media(url='https://pbs.twimg.com/media/EtZOKUiWgAIeqtD.jpg', type='photo')], hashtags=[], mentions=[], urls=[])
    Tweet(created_at=<Arrow [2019-04-10T14:01:13+00:00]>, id_str='1115978039534297088', conversation_id_str='1115978039534297088', full_text='ブラックホールの画像にめちゃくちゃ既視感があったので、ナンだろうと思ったら、心筋シンチの短軸断層像だった。これからするとブラックホールは前壁中隔の虚血が疑われますね。冠動脈造影検査が考慮されます。 https://t.co/8aa4lbiGNt', lang='ja', favorited=False, retweeted=False, retweet_count=2429, favorite_count=4665, reply_count=12, quote_count=41, quoted_status_id_str='', quoted_status_short_url='', quoted_status_expand_url='', user_id_str='119999913', user_name='naikabucho', user_full_name='内科部長（脱メタル）', user_verified=False, in_reply_to_status_id_str='', in_reply_to_user_id_str='', media=[Media(url='https://pbs.twimg.com/media/D3y6-_7UwAIvHtm.jpg', type='photo'), Media(url='https://pbs.twimg.com/media/D3y8KwvUwAEy0A4.jpg', type='photo')], hashtags=[], mentions=[], urls=[])


The result of task show how many tweets scrapped and how many can’t.

.. code:: python

    run_result




.. parsed-literal::

    TweetsByIdsResult(downloaded_count=2, tweet_ids_not_scrapped=['56546745646545646574'])



