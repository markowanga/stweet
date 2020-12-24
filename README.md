# stweet

![Python package](https://github.com/markowanga/stweet/workflows/Python%20package/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/markowanga/stweet/branch/master/graph/badge.svg?token=1PV6VC8HRF)](https://codecov.io/gh/markowanga/stweet)
[![PyPI version](https://badge.fury.io/py/stweet.svg)](https://badge.fury.io/py/stweet)

A modern fast python library to scrap tweets and users quickly from Twitter unofficial API.

This tool helps you to scrap tweets by a search phrase, tweets by ids and user by usernames. It uses the Twitter API,
the same API is used on a website.

## Inspiration for the creation of the library

I have used twint to scrap tweets, but it has many errors, and it doesn't work properly. The code was not simple to
understand. All tasks have one config, and the user has to know the exact parameter. The last important thing is the
fact that Api can change — Twitter is the API owner and changes depend on it. It is annoying when something does not
work and users must report bugs as issues.

## Main advantages of the library

- **Simple code** — the code is not only mine, every user can contribute to the library
- **Domain objects and interfaces** — the main part of functionalities can be replaced (eg. calling web requests), the
  library has basic simple solution — if you want to expand it, you can do it without any problems and forks
- **100% coverage with integration tests** — this advantage can find the API changes, tests are carried out every week
  and when the task fails, we can find the source of change easily
- **Custom tweets and users output** — it is a part of the interface, if you want to save tweets and users custom
  format, it takes you a brief moment

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

This simple code snippet calls for all tweets with hashtag **#covid19**. The result in **tweets** object is a list of
scrapped tweets.

Above example shows how to scrap tweets by search phrase. Stweet has also scrapping by tweet id:

```python
import stweet as st

tweets_by_ids_task = st.TweetsByIdsTask(['1336002732717727752', '1338916735479496704'])
tweets_collector = st.CollectorTweetOutput()

st.TweetsByIdsRunner(
    tweets_by_ids_task=tweets_by_ids_task,
    tweet_outputs=[tweets_collector, st.CsvTweetOutput('output_file.csv')]
).run()

tweets = tweets_collector.get_scrapped_tweets()
```

Stweet allows scrapping user information by users screen name:

```python
import stweet as st

get_users_task = st.GetUsersTask(['donaldtuskEPP', 'JoeBiden', 'realDonaldTrump'])
users_collector = st.CollectorUserOutput()

st.GetUsersRunner(
    get_user_task=get_users_task,
    user_outputs=[users_collector]
).run()

users = users_collector.get_scrapped_users()
```

Stweet has a default `WebClient` implementation that is based on `requests` library — `st.RequestsWebClient`. Class have
all properties with default values, but by changing them user can set proxy or disable ssl verification.

This snippet shows how to use it:

```python
import stweet as st

search_tweets_task = st.SearchTweetsTask(
    all_words='#covid19',
)
tweets_collector = st.CollectorTweetOutput()

proxies_config = st.RequestsWebClientProxyConfig(
    http_proxy="<Your http proxy URL>",
    https_proxy="<Your https proxy URL>"
)

st.TweetSearchRunner(
    search_tweets_task=search_tweets_task,
    tweet_outputs=[tweets_collector, st.CsvTweetOutput('output_file.csv')],
    web_client=st.RequestsWebClient(proxy=proxies_config, verify=False),
).run()

tweets = tweets_collector.get_scrapped_tweets()
```

All important details and classes of this library are described below.

## SearchTweetsTask

This class represents the task to scrap tweets. It contains the following properties:

|Property|Type|Description|
|---|---|---|
|all_words|Optional[str]|Search for tweets having all words in property|
|exact_words|Optional[str]|Search for tweets with the unchanged order of words in property|
|any_word|Optional[str]|Search for tweets with any words in this property|
|from_username|Optional[str]|Search for tweets from the user|
|to_username|Optional[str]|Search for tweets to the user (tweets starts from mentioning the user)|
|since|Optional[Arrow]|Search for tweets since time|
|until|Optional[Arrow]|Search for tweets until time|
|language|Optional[st.Language]|Search for tweets with language|
|tweets_count|Optional[int]|Search first tweets_count tweets|
|replies_filter|Optional[st.RepliesFilter]|Filter tweets with reply/original status|

All properties come from **Twitter advanced search** and are default None.

## SearchRunner

With class SearchRunner library can scrap tweets specified in SearchTweetsTask. The runner has the following properties:

|Property|Type|Default value|Description|
|---|---|---|---|
|search_run_context|st.SearchRunContext|None, in \_\_init\_\_() assign SearchRunContext()|Search context, contains all important properties to make the next request to Twitter|
|search_tweets_task|st.SearchTweetsTask|**Obligatory property**|Property specifies which tweets should be downloaded by the runner|
|tweet_outputs|List[st.TweetOutput]|**Obligatory property**|List of objects to export downloaded tweets|
|web_client|st.WebClient|stweet.http_request.WebClientRequests()|Implementation of a WebClient, can be replaced for custom implementation|
|tweet_parser|st.TweetParser|stweet.parse.TwintBasedTweetParser()|Parser of tweets from web API response|
|auth_token_provider_factory|st.auth.AuthTokenProviderFactory|st.auth.SimpleAuthTokenProviderFactory()|Factory of AuthTokenProvider to provide auth tokens|

## TweetsByIdsTask

This class represents the task to scrap tweets by ids, it has simple property:

|Property|Type|Description|
|---|---|---|
|tweet_ids|List[str]|ids of tweets to scrap|

## TweetsByIdsRunner

With class TweetsByIdsRunner library can scrap tweets specified in TweetsByIdsTask. The runner has the following
properties:

|Property|Type|Default value|Description|
|---|---|---|---|
|tweets_by_ids_task|st.TweetsByIdsTask|**Obligatory property**|Property specifies which tweets should be downloaded by the runner|
|tweet_outputs|List[st.TweetOutput]|**Obligatory property**|List of objects to export downloaded tweets|
|search_run_context|st.SearchRunContext|None, in \_\_init\_\_() assign SearchRunContext()|Search context, contains all important properties to make the next request to Twitter|
|web_client|st.WebClient|stweet.http_request.WebClientRequests()|Implementation of a WebClient, can be replaced for custom implementation|
|tweet_parser|st.TweetParser|stweet.parse.TwintBasedTweetParser()|Parser of tweets from web API response|
|auth_token_provider_factory|st.auth.AuthTokenProviderFactory|st.auth.SimpleAuthTokenProviderFactory()|Factory of AuthTokenProvider to provide auth tokens|

## GetUsersTask

This class represents the task to scrap users, it has simple property:

|Property|Type|Description|
|---|---|---|
|usernames|List[str]|usernames of users to scrap, username is usually used in Twitter with '@' prefix|

## GetUsersRunner

With class GetUsersRunner library can scrap users specified in GetUsersTask. The runner has the following properties:

|Property|Type|Default value|Description|
|---|---|---|---|
|get_user_task|st.GetUsersTask|**Obligatory property**|Property specifies which users should be downloaded by the runner|
|user_outputs|List[st.UserOutput]|**Obligatory property**|List of objects to export downloaded users|
|get_user_context|st.GetUsersContext|None, in \_\_init\_\_() assign GetUsersContext()|Search context, contains all important properties to make the next request to Twitter|
|web_client|st.WebClient|stweet.http_request.WebClientRequests()|Implementation of a WebClient, can be replaced for custom implementation|
|auth_token_provider_factory|st.auth.AuthTokenProviderFactory|st.auth.SimpleAuthTokenProviderFactory()|Factory of AuthTokenProvider to provide auth tokens|

## TweetOutput

TweetOutput is an interface which calls for exporting scrapped tweets. Stweet has a few implementations described below:

|TweetOutput implementation|Description|
|---|---|
|CollectorTweetOutput|Output saves tweets in-memory, has the method **get_scrapped_tweets()** to return list of tweets|
|CsvTweetOutput|Output exports tweets to csv file|
|JsonLineFileTweetOutput|Output exports tweets as JSON objects, in each line of file there is one JSON object with a tweet|
|PrintEveryNTweetOutput|Output prints every N tweet on screen, N value can be assigned in the constructor|
|PrintFirstInRequestTweetOutput|Output prints the first tweet of an incoming request|
|PrintTweetOutput|Output prints all tweets|

Additionally, TweetOutput can be implemented in many other ways.

## UserOutput

UserOutput is an interface which calls for exporting scrapped users. Stweet has a few implementations described below:

|UserOutput implementation|Description|
|---|---|
|CollectorUserOutput|Output saves users in-memory, has the method **get_scrapped_users()** to return list of users|
|CsvUserOutput|Output exports users to csv file|
|JsonLineFileUserOutput|Output exports users as JSON objects, in each line of file there is one JSON object with a user|
|PrintEveryNUserOutput|Output prints every N user on screen, N value can be assigned in the constructor|
|PrintFirstInRequestUserOutput|Output prints the first user of an incoming request|
|PrintUserOutput|Output prints all users|

Additionally, UserOutput can be implemented in many other ways.

## ProxyClientRequests

`ProxyClientRequests` is an implementation of a `st.WebClient` that allows using proxies as well as supply additional
options that can be used in [requests.request](https://requests.readthedocs.io/en/latest/api/#requests.request) method.

|Property|Type|Description|
|---|---|---|
|proxies|Dict[str, str]|Dictionary mapping protocol to the URL of the proxy.|
|options|Dict[str, Any]|Dictionary mapping a `requests.request` method param to its value.

Additionally, you can implement you own WebClient.

## How to contribute

If you want to improve stweet library then please read the instruction
in [first-contributions repo](https://github.com/firstcontributions/first-contributions). Remember to create pull
request to `develop` branch.

You must have `docker` and `docker-compose` to run all tests on your computer. These dependencies start the proxy
service which is required to run proxy tests. If you want to run tests locally please run `tox` command:

```bash
tox -v
```

Thank you for your every pull request. Together we can make this library better.

## Twint inspiration

Small part of library uses code from [twint](https://github.com/twintproject/twint). Twint was also main inspiration to
create stweet.
