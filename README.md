# [WIP] stweet

![Python package](https://github.com/markowanga/stweet/workflows/Python%20package/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/markowanga/stweet/branch/master/graph/badge.svg?token=1PV6VC8HRF)](https://codecov.io/gh/markowanga/stweet)
[![PyPI version](https://badge.fury.io/py/stweet.svg)](https://badge.fury.io/py/stweet)

A modern fast python library to scrap tweets quickly from Twitter unofficial API.

This tool helps you to scrap tweet by a search phrase. It uses the twitter API, the same API is used on website.

## Inspiration for the creation of the library
I have used twint to scrap tweets, but it has many errors and it doesn't work properly. 
The code was not simple to understand. All tasks have one config and the user has to know the exact parameter.
The last important thing is the fact that Api can change — Twitter is the API owner and changes depend on it. 
It is annoying when something does not work and users must report bugs as issues.

## Main advantages of the library
 - **Simple code** — the code is not only mine, every user can contribute to the library
 - **Domain objects and interfaces** — the main part of functionalities can be replaced (eg. calling web requests),
   the library has basic simple solution — if you want to expand it, you can do it without any problems and forks
 - **100% coverage with integration tests** — this advantage can find the API changes, 
   tests are carried out every week and when the task fails, we can find the source of change easily
 - **Custom tweets output** — it is a part of the interface, if you want to save custom tweets, 
   it takes you a brief moment
   
## Installation
```shell script
pip install -U stweet
```

## Basic usage
To make a simple request the scrap **task** must be prepared. The next task should be processed by **runner**.
```python
import stweet as st

search_tweets_task = st.SearchTweetsTask(
    all_words='#covid19'
)

tweets_collector = st.CollectorTweetOutput()

st.TweetSearchRunner(
    search_tweets_task=search_tweets_task,
    tweet_outputs=[tweets_collector, st.CsvTweetOutput('output_file.csv')]
).run()

tweets = tweets_collector.get_scrapped_tweets()
```
This simple code snippet calls for all tweets with hashtag **#covid19**.
The result in **tweets** object is a list of scrapped tweets. 
All important details of this library are described below.

## SearchTweetsTask
This class represents the task to scrap tweets. It contains the following properties:

|Property|Type|Default value|Description|
|---|---|---|---|
|all_words|Optional[str]|None|Search for tweets having all words in property|
|exact_words|Optional[str]|None|Search for tweets with the unchanged order of words in property|
|any_word|Optional[str]|None|Search for tweets with any words in this property|
|from_username|Optional[str]|None|Search for tweets from the user|
|to_username|Optional[str]|None|Search for tweets to the user (tweets starts from mentioning the user)|
|since|Optional[Arrow]|None|Search for tweets since time|
|until|Optional[Arrow]|None|Search for tweets until time|
|language|Optional[st.Language]|None|Search for tweets with language|
|tweets_count|Optional[int]|None|Search first tweets_count tweets|
|replies_filter|Optional[st.RepliesFilter]|None|Filter tweets with reply/original status|

All properties come from **Twitter advanced search** and are default None.

## SearchRunner
With class SearchRunner library can scrap tweets specified in SearchTweetsTask.
The runner has the following properties:

|Property|Type|Default value|Description|
|---|---|---|---|
|search_run_context|st.SearchRunContext|None, in \_\_init\_\_() assign SearchRunContext()|Search context, contains all important properties to make the next request to Twitter|
|search_tweets_task|st.SearchTweetsTask|**Obligatory property**|Property specifies which tweets should be downloaded by the runner|
|tweet_outputs|List[st.TweetOutput]|**Obligatory property**|List of objects to export downloaded tweets|
|web_client|st.WebClient|stweet.http_request.WebClientRequests|Implementation of a WebClient, can be replaced for custom implementation|
|tweet_parser|st.TweetParser|stweet.parse.TwintBasedTweetParser|Parser of tweets from web API response|

## TweetOutput
TweetOutput is an interface which calls for exporting scrapped tweets. 
Stweet has a few implementations described below:

|TweetOutput implementation|Description|
|---|---|
|CollectorTweetOutput|Output saves tweets in-memory, has the method **get_scrapped_tweets()** to return list of tweets|
|CsvTweetOutput|Output exports tweets to csv file|
|JsonLineFileTweetOutput|Output exports tweets as JSON objects, in each line of file there is one JSON object with a tweet|
|PrintEveryNTweetOutput|Output prints every N tweet on screen, N value can be assigned in the constructor|
|PrintFirstInRequestTweetOutput|Output prints the first tweet of an incoming request|
|PrintTweetOutput|Output prints all tweets|

Additionally, TweetOutput can be implemented in many other ways.

## Known problems
 - Sometimes when Github Actions run, auth token from Twitter does not income. 
   Then the integration test fails. In this case the best solution is to repeat the test

## Twint inspiration
Small part of library uses code from [twint](https://github.com/twintproject/twint). 
Twint was also main inspiration to create stweet.
