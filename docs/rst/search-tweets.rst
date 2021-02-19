Download searched tweets
========================

.. code:: python

    import stweet as st

Prepare task
------------

Task named ``SearchTweetsTask`` have many properties: -
**``all_words: Optional[str]``** – tweets have all words, not exactly in
one block of text - **``exact_words: Optional[str]``** – tweets have all
words in exact order - **``any_word: Optional[str]``** – tweets have at
least one word - **``from_username: Optional[str]``** – tweets are
posted by username - **``to_username: Optional[str]``** – tweets are
posted to username - **``since: Optional[Arrow]``** – tweets since time
- **``until: Optional[Arrow]``** – tweets until time -
**``language: Optional[Language]``** – tweets from language, only one
language can be selected - **``tweets_limit: Optional[int]``** – limit
to first N scrapped tweets -
**``replies_filter: Optional[RepliesFilter]``** – filter tweets by
replies or original tweets, when None there is no filter

.. code:: python

    task = st.SearchTweetsTask(
        all_words='#covid19', 
        tweets_limit=100, 
        language=st.Language.POLISH,
        replies_filter=st.RepliesFilter.ONLY_ORIGINAL
    )

Prepare TweetOutputs
--------------------

Here is example of use TweetOutputs. All options are in tweet-output
section.

.. code:: python

    tweet_outputs = [
        st.JsonLineFileTweetOutput('example.jl')
    ]

Example task execution
----------------------

The base configuration of ``TweetSearchRunner`` needs
``search_tweets_task`` and ``tweet_outputs``. To execute runner object
you need to execute ``run()`` method.

.. code:: python

    run_result = st.TweetSearchRunner(
        search_tweets_task=task, 
        tweet_outputs=tweet_outputs
    ).run()

``TweetSearchRunner`` returns ``SearchTweetsResult`` which contain the
count of scrapped tweets.

.. code:: python

    run_result




.. parsed-literal::

    SearchTweetsResult(downloaded_count=100)



More about ``TweetSearchRunner`` configuration
----------------------------------------------

Here are all properties of ``TweetSearchRunner``: -
**``search_tweets_task: SearchTweetsTask``** – task with definition of
tweets to scrap - **``tweet_outputs: List[TweetOutput]``** – objects to
export scrapped tweets -
**``search_run_context: Optional[SearchRunContext] = None``** – context
of scrapping, it can continoue the paused scrapping or put initial auth
token, if None the basic context is provided -
**``web_client: WebClient = RequestsWebClient()``** – client to execute
web connections, here can be configure proxy connection for example -
**``tweet_parser: TweetParser = BaseTweetParser()``** – parser of tweet
response from Twitter -
**``auth_token_provider_factory: AuthTokenProviderFactory = SimpleAuthTokenProviderFactory()``**
– provider of auth token

