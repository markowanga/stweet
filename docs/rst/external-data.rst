External data
=============

This module show how to manage tweets with external files.

Library have 2 domain objects: - Tweet - User

This objects are DTO’s of data scrapped with stweet library.

.. code:: ipython3

    import stweet as st
    from typing import List

.. code:: ipython3

    def get_some_tweets() -> List[st.Tweet]:
        task = st.SearchTweetsTask('#covid19', tweets_limit=10)
        tweets_collector = st.CollectorTweetOutput()
        st.TweetSearchRunner(task, [tweets_collector]).run()
        return tweets_collector.get_scrapped_tweets()

.. code:: ipython3

    def get_some_users() -> List[st.Tweet]:
        usernames = ['ProtasiewiczJ', 'donaldtuskEPP']
        task = st.GetUsersTask(usernames)
        user_collector = st.CollectorUserOutput()
        task_result = st.GetUsersRunner(task, [user_collector]).run()
        return user_collector.get_scrapped_users()

.. code:: ipython3

    some_tweets = get_some_tweets()
    some_users = get_some_users()

Tweet
-----

Currently there are two external storage of tweets: - CSV file - JSON
lines file

All formats have import and export methods.

Export tweets to CSV file
~~~~~~~~~~~~~~~~~~~~~~~~~

Method ``export_tweets_to_csv`` needs two parameters: -
**``tweets: List[Tweet]``** – list of tweets to export -
**``filename: str``** – destination file

.. code:: ipython3

    st.export_tweets_to_csv(some_tweets, 'tweets.csv')

Export tweets to JSON line file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Method ``export_tweets_to_json_lines`` needs two parameters: -
**``tweets: List[Tweet]``** – list of tweets to export -
**``filename: str``** – destination file

.. code:: ipython3

    st.export_tweets_to_json_lines(some_tweets, 'tweets.jl')

Import tweets from CSV file
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Method ``read_tweets_from_csv_file`` have parameter: -
**``file_path: str``** – destination file

Method returns ``List[Tweet]``

.. code:: ipython3

    tweets = st.read_tweets_from_csv_file('tweets.csv')

Import tweets from JSON lines file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Method ``read_tweets_from_json_lines_file`` have parameter: -
**``file_path: str``** – destination file

Method returns ``List[Tweet]``

.. code:: ipython3

    tweets = st.read_tweets_from_json_lines_file('tweets.jl')

User
----

Currently there are two external storage of users: - CSV file - JSON
lines file

All formats have import and export methods.

Export users to CSV file
~~~~~~~~~~~~~~~~~~~~~~~~

Method ``export_users_to_csv`` needs two parameters: -
**``users: List[User]``** – list of users to export -
**``filename: str``** – destination file

.. code:: ipython3

    st.export_users_to_csv(some_users, 'users.csv')

Export users to JSON line file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Method ``export_users_to_json_lines`` needs two parameters: -
**``users: List[User]``** – list of users to export -
**``filename: str``** – destination file

.. code:: ipython3

    st.export_users_to_json_lines(some_users, 'users.jl')

Import users from CSV file
~~~~~~~~~~~~~~~~~~~~~~~~~~

Method ``read_users_from_csv_file`` have parameter: -
**``file_path: str``** – destination file

Method returns ``List[User]``

.. code:: ipython3

    users = st.read_users_from_csv_file('users.csv')

Import users from JSON lines file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Method ``read_users_from_json_lines_file`` have parameter: -
**``file_path: str``** – destination file

Method returns ``List[User]``

.. code:: ipython3

    tweets = st.read_users_from_json_lines_file('users.jl')

