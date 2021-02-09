Tweet output
============

``TweetOutput`` is as generic class which can export scrapped tweets.

Under the hood it has abstract method
``export_tweets(tweets: List[Tweet])``.

There are few implementations of ``TweetOutput``

.. code:: ipython3

    import stweet as st

PrintTweetOutput
----------------

PrintTweetOutput prints all tweets in console. It does not store tweets
anywhere.

.. code:: ipython3

    st.PrintTweetOutput();




.. parsed-literal::

    <stweet.tweet_output.print_tweet_output.PrintTweetOutput at 0x7ff4b42a6d00>



CollectorTweetOutput
--------------------

CollectorTweetOutput stores all tweets in memory. This solution is best
way when we want to analyse small part of tweets.

To get all tweets run method ``get_scrapped_tweets()``

.. code:: ipython3

    st.CollectorTweetOutput();




.. parsed-literal::

    <stweet.tweet_output.collector_tweet_output.CollectorTweetOutput at 0x7ff4b42a6a60>



CsvTweetOutput
--------------

``CsvTweetOutput`` stores tweets in csv file. It has two parameters
``file_location`` and ``add_header_on_start``.

When ``add_header_on_start`` is ``True`` header is adding only when file
is empty. It is possible to continue storing the tweets in file in next
tasks.

.. code:: ipython3

    st.CsvTweetOutput(
        file_location='my_csv_file.csv',
        add_header_on_start=True
    );




.. parsed-literal::

    <stweet.tweet_output.csv_tweet_output.CsvTweetOutput at 0x7ff4b586bf10>



JsonLineFileTweetOutput
-----------------------

``JsonLineFileTweetOutput`` stores tweets in file in json lines. This
solution is better because it can be problem with fast saving new tweet
in large files, also it can be problem with reading. Using json lines it
is possible to read line by line, without read whole document into
memory.

Class have only one property – ``file_name``, this is the file to store
tweets in json line format.

.. code:: ipython3

    st.JsonLineFileTweetOutput(
        file_name='my_jl_file.jl'
    );




.. parsed-literal::

    <stweet.tweet_output.json_line_file_tweet_output.JsonLineFileTweetOutput at 0x7ff4b42a62e0>



PrintEveryNTweetOutput
----------------------

``PrintEveryNTweetOutput`` print event N-th scrapped tweet. This is best
solution to track that new tweets are scrapping.

Class have only one parameter – ``each_n``, this is the N value
described above.

.. code:: ipython3

    st.PrintEveryNTweetOutput(
        each_n=1000
    );




.. parsed-literal::

    <stweet.tweet_output.print_every_n_tweet_output.PrintEveryNTweetOutput at 0x7ff4b42a6970>



PrintFirstInRequestTweetOutput
------------------------------

PrintFirstInRequestTweetOutput is a debug TweetOutput. It allow to track
every request and shows the first part of response.

.. code:: ipython3

    st.PrintFirstInRequestTweetOutput();




.. parsed-literal::

    <stweet.tweet_output.print_first_in_request_tweet_output.PrintFirstInRequestTweetOutput at 0x7ff4b586b8b0>


