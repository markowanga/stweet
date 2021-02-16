Examples of usage
=================

Here are simple examples of using stweet

.. code:: python

    import stweet as st
    import arrow

1. Scrap tweets
---------------

Example 1.1.
~~~~~~~~~~~~

Scrap tweets with ``#covid19`` between
``'2020-05-11T20:00:00.000+01:00'`` and
``'2020-05-11T20:01:00.000+01:00'``. Collect all tweets in memory and
save to CSV file.

.. code:: python

    task = st.SearchTweetsTask(
        '#covid19',
        since=arrow.get('2020-05-11T20:00:00.000+01:00'),
        until=arrow.get('2020-05-11T20:01:00.000+01:00')
    )
    tweets_collector = st.CollectorTweetOutput()
    result = st.TweetSearchRunner(task, [tweets_collector, st.CsvTweetOutput('covid19_tweets.csv')]).run()
    print(f'scrapping task result: {result}')


.. parsed-literal::

    scrapping task result: SearchTweetsResult(downloaded_count=465)


.. code:: python

    print('first tweet content:')
    print(tweets_collector.get_scrapped_tweets()[0].full_text)


.. parsed-literal::

    first tweet content:
    We have compiled a list of hotlines, websites, and other support services that you may find helpful during this uncertain time:
    https://t.co/i6Hn1JjIBT 
    #JVS #JCFS #HereForYou #communityresources #advocacy #COVID19 #coronavirus #coping https://t.co/nA0CDn8QyT


.. code:: python

    print(f'first tweet time: {tweets_collector.get_scrapped_tweets()[0].created_at}')


.. parsed-literal::

    first tweet time: 2020-05-11T19:00:59+00:00


Scrapped time have different hour than was input in task, but everything
is ok because scrapped tweet has no time offset.

Example 1.2.
~~~~~~~~~~~~

Scrap first 70 tweets with exact phrase ``crypto is awesome`` and save
them in memory and in JSON lines file.

.. code:: python

    task = st.SearchTweetsTask(
        exact_words='crypto is awesome',
        tweets_limit=70
    )
    tweets_collector = st.CollectorTweetOutput()
    result = st.TweetSearchRunner(task, [tweets_collector, st.JsonLineFileTweetOutput('covid19_tweets.jl')]).run()
    print(f'scrapping task result: {result}')


.. parsed-literal::

    scrapping task result: SearchTweetsResult(downloaded_count=70)


.. code:: python

    print('first tweet content:')
    print(tweets_collector.get_scrapped_tweets()[0].full_text)


.. parsed-literal::

    first tweet content:
    Just scalped $1,500+ on $VTHO before bed.
    
    Crypto is awesome.


.. code:: python

    print('last tweet content:')
    print(tweets_collector.get_scrapped_tweets()[-1].full_text)


.. parsed-literal::

    last tweet content:
    @RuleXRP The speed of.crypto is awesome though.


Example 1.3.
~~~~~~~~~~~~

Scrap first 1000 tweets with any of hashtags: ``#covid19`` or ``#bbc``
using proxy. Save it in memory.

.. code:: python

    task = st.SearchTweetsTask(
        any_word='#covid19 #bbc',
        tweets_limit=1000
    )
    web_client = st.RequestsWebClient(
        proxy=st.RequestsWebClientProxyConfig(http_proxy='', https_proxy='')
    )
    tweets_collector = st.CollectorTweetOutput()
    result = st.TweetSearchRunner(task, [tweets_collector], web_client=web_client).run()
    print(f'scrapping task result: {result}')


.. parsed-literal::

    scrapping task result: SearchTweetsResult(downloaded_count=1000)


Twitter index hashtags without case sensitive. There is a need to create
simple function to check that tweet contains hashtag.

.. code:: python

    def tweet_cointain_hashtag(tweet: st.Tweet, hashtag: str) -> bool:
        return hashtag.lower() in tweet.full_text.lower()

.. code:: python

    tweets = tweets_collector.get_scrapped_tweets()
    
    print('both count:', len([
        it for it in tweets 
        if tweet_cointain_hashtag(it, '#bbc') and tweet_cointain_hashtag(it, '#covid19')
    ]))
    print('only #covid19 count:', len([it for it in tweets if tweet_cointain_hashtag(it, '#covid19')]))
    print('only #bbc count:', len([it for it in tweets if tweet_cointain_hashtag(it, '#bbc')]))


.. parsed-literal::

    both count: 0
    only #covid19 count: 977
    only #bbc count: 20


Example 1.4.
~~~~~~~~~~~~

Scrap tweets by ids and save in memory, check that all are existing.

.. code:: python

    task = st.TweetsByIdsTask(['1337071849772093442', '1337067073051238400'])
    tweets_collector = st.CollectorTweetOutput()
    
    result = st.TweetsByIdsRunner(task, [tweets_collector]).run()
    scrapped_tweets_ids = [it.id_str for it in tweets_collector.get_scrapped_tweets()]
    
    print('tweet ids not scrapped:', result.tweet_ids_not_scrapped)
    print('scrapped tweets count:', len(tweets_collector.get_scrapped_tweets()))


.. parsed-literal::

    tweet ids not scrapped: ['1337067073051238400']
    scrapped tweets count: 1


2. Scrap users
--------------

Example 2.1.
~~~~~~~~~~~~

Scrap users by usernames. Save them into memry, CSV and JSON lines.

.. code:: python

    usernames = ['ProtasiewiczJ', 'donaldtuskEPP']
    task = st.GetUsersTask(usernames)
    
    user_collector = st.CollectorUserOutput()
    outputs = [
        st.CsvUserOutput('users.csv'),
        st.JsonLineFileUserOutput('users.jl'),
        user_collector
    ]
    
    task_result = st.GetUsersRunner(task, outputs).run()
    [it.screen_name for it in user_collector.get_scrapped_users()]




.. parsed-literal::

    ['ProtasiewiczJ', 'donaldtuskEPP']



3. Export data
--------------

Example 3.1.
~~~~~~~~~~~~

Export previous scrapped tweets into CSV and JSON line file.

.. code:: python

    tweets = tweets_collector.get_scrapped_tweets()
    st.export_tweets_to_csv(tweets, 'export_tweets.csv')
    st.export_tweets_to_json_lines(tweets, 'export_tweets.jl')

Example 3.2.
~~~~~~~~~~~~

Export previous scrapped users into CSV and JSON line file.

.. code:: python

    users = user_collector.get_scrapped_users()
    st.export_users_to_csv(users, 'export_users.csv')
    st.export_users_to_json_lines(users, 'export_users.jl')

4. Import data
--------------

Example 4.1.
~~~~~~~~~~~~

Import tweets from JSON lines file.

.. code:: python

    tweets = st.read_tweets_from_json_lines_file('export_tweets.jl')

Example 4.2.
~~~~~~~~~~~~

Import tweets from CSV file.

.. code:: python

    tweets = st.read_tweets_from_csv_file('export_tweets.csv')

Example 4.3.
~~~~~~~~~~~~

Import users from JSON lines file.

.. code:: python

    users = st.read_users_from_json_lines_file('export_users.jl')

Example 4.4.
~~~~~~~~~~~~

Import users from CSV file.

.. code:: python

    users = st.read_users_from_csv_file('export_users.csv')

