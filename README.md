# [WIP] stweet

![Python package](https://github.com/markowanga/stweet/workflows/Python%20package/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/markowanga/stweet/branch/master/graph/badge.svg?token=1PV6VC8HRF)](https://codecov.io/gh/markowanga/stweet)


Modern fast python library to quickly scrap tweets from Twitter unofficial API.

This tool helps you to scrap tweet by search phrase. It uses the twitter api, same api is used on website.

## Inspiration for the creation of the library
I have used twint to scrap tweets, but it have many errors it doesn't work correct. 
The code was not simple to understand. All tasks have one config and user must know what exactly parameter is.
Last important thing is fact that api can change — Twitter is api owner and changes are dependent of them. 
It is annoying when something does not work and users must report bugs is issues.

## Main advantages of the solution
 - Simple code — code is not mine, every user can contribute library
 - Domain objects and interfaces — main part of functionalities can be replaced (eg. calling web requests),
   library have basic simple solution, if you want to expand it you can do it very simple
 - 100% coverage with integration tests — this can find the api changes, 
   tests is run every week and when task is failed we can easily find the source of change
 - Custom tweets output — it's part of interface, it you want to save custom tweets it takes you a short moment

## Basic usage
To make simple request the scrap task must be prepared. Next task should be processed by runner.
```python
import stweet as st

search_tweets_task = st.SearchTweetsTask(
    all_words='#covid19',
    tweets_count=5
)
tweets_collector = st.CollectorTweetOutput()
st.TweetSearchRunner(
    search_tweets_task=search_tweets_task,
    tweet_outputs=[tweets_collector, st.CsvTweetOutput('output_file.csv')]
).run()
tweets = tweets_collector.get_scrapped_tweets()
```
