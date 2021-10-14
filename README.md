# stweet

[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
![Python package](https://github.com/markowanga/stweet/workflows/Python%20package/badge.svg?branch=master)
[![PyPI version](https://badge.fury.io/py/stweet.svg)](https://badge.fury.io/py/stweet)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

A modern fast python library to scrap tweets and users quickly from Twitter unofficial API.

This tool helps you to scrap tweets by a search phrase, tweets by ids and user by usernames. It uses
the Twitter API, the same API is used on a website.

## Inspiration for the creation of the library

I have used twint to scrap tweets, but it has many errors, and it doesn't work properly. The code
was not simple to understand. All tasks have one config, and the user has to know the exact
parameter. The last important thing is the fact that Api can change — Twitter is the API owner and
changes depend on it. It is annoying when something does not work and users must report bugs as
issues.

## Main advantages of the library

- **Simple code** — the code is not only mine, every user can contribute to the library
- **Domain objects and interfaces** — the main part of functionalities can be replaced (eg. calling
  web requests), the library has basic simple solution — if you want to expand it, you can do it
  without any problems and forks
- ~~**100% coverage with integration tests** — this advantage can find the API changes, tests are
  carried out every week and when the task fails, we can find the source of change easily~~ – not in
  version 2.0
- **Custom tweets and users output** — it is a part of the interface, if you want to save tweets and
  users custom format, it takes you a brief moment

## Installation

```shell script
pip install -U stweet
```

## Donate

If you want to sponsor me, in thanks for the project, please send me some crypto 😁:

|Coin|Wallet address|
|---|---|
|Bitcoin|3EajE9DbLvEmBHLRzjDfG86LyZB4jzsZyg|
|Etherum|0xE43d8C2c7a9af286bc2fc0568e2812151AF9b1FD|

## Basic usage

To make a simple request the scrap **task** must be prepared. The task should be processed by **
runner**.

```python
import stweet as st


def try_search():
    search_tweets_task = st.SearchTweetsTask(all_words='#covid19')
    output_jl_tweets = st.JsonLineFileRawOutput('output_raw_search_tweets.jl')
    output_jl_users = st.JsonLineFileRawOutput('output_raw_search_users.jl')
    output_print = st.PrintRawOutput()
    st.TweetSearchRunner(search_tweets_task=search_tweets_task,
                         tweet_raw_data_outputs=[output_print, output_jl_tweets],
                         user_raw_data_outputs=[output_print, output_jl_users]).run()


def try_user_scrap():
    user_task = st.GetUsersTask(['iga_swiatek'])
    output_json = st.JsonLineFileRawOutput('output_raw_user.jl')
    output_print = st.PrintRawOutput()
    st.GetUsersRunner(get_user_task=user_task, raw_data_outputs=[output_print, output_json]).run()


def try_tweet_by_id_scrap():
    id_task = st.TweetsByIdTask('1447348840164564994')
    output_json = st.JsonLineFileRawOutput('output_raw_id.jl')
    output_print = st.PrintRawOutput()
    st.TweetsByIdRunner(tweets_by_id_task=id_task,
                        raw_data_outputs=[output_print, output_json]).run()


if __name__ == '__main__':
    try_search()
    try_user_scrap()
    try_tweet_by_id_scrap()
```

Example above shows that it is few lines of code required to scrap tweets.

## Export format

Stweet uses api from website so there is no documentation about receiving response. Response is
saving as raw so final user must parse it on his own. Maybe parser will be added in feature.

Scrapped data can be exported in different ways by using `RawDataOutput` abstract class. List of
these outputs can be passed in every runner – yes it is possible to export in two different ways.

Currently, stweet have implemented:

- **CollectorRawOutput** – can save data in memory and return as list of objects
- **JsonLineFileRawOutput** – can export data as json lines
- **PrintEveryNRawOutput** – prints every N-th item
- **PrintFirstInBatchRawOutput** – prints first item in batch
- **PrintRawOutput** – prints all items (not recommended in large scrapping)

## Using tor proxy
Library is integrated with [tor-python-easy](https://github.com/markowanga/tor-python-easy).
It allows using tor proxy with exposed control port – to change ip when it is needed.

If you want to use tor proxy client you need to prepare custom web client and use it in runner.

You need to run tor proxy -- you can run it on your local OS, or you can use this 
[docker-compose](https://github.com/markowanga/tor-python-easy/blob/main/docker-compose.yml).

Code snippet below show how to use proxy:
```python
import stweet as st

if __name__ == '__main__':
    web_client = st.DefaultTwitterWebClientProvider.get_web_client_preconfigured_for_tor_proxy(
        socks_proxy_url='socks5://localhost:9050',
        control_host='localhost',
        control_port=9051,
        control_password='test1234'
    )

    search_tweets_task = st.SearchTweetsTask(all_words='#covid19')
    output_jl_tweets = st.JsonLineFileRawOutput('output_raw_search_tweets.jl')
    output_jl_users = st.JsonLineFileRawOutput('output_raw_search_users.jl')
    output_print = st.PrintRawOutput()
    st.TweetSearchRunner(search_tweets_task=search_tweets_task,
                         tweet_raw_data_outputs=[output_print, output_jl_tweets],
                         user_raw_data_outputs=[output_print, output_jl_users],
                         web_client=web_client).run()
```

## Twint inspiration

Small part of library uses code from [twint](https://github.com/twintproject/twint). Twint was also
main inspiration to create stweet.
