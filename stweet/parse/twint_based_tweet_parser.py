"""Utils to parse data from web response."""

import json
from datetime import datetime
from typing import List, Optional

from . import TweetParser
from ..model.tweet import Tweet

_Tweet_formats = {
    'datetime': '%Y-%m-%d %H:%M:%S %Z',
    'datestamp': '%Y-%m-%d',
    'timestamp': '%H:%M:%S'
}


class TwintBasedTweetParser(TweetParser):
    """Utils class to parse data from web response."""

    def parse_tweets(self, response_text: str) -> List[Tweet]:
        """Method to extract tweets from web response."""
        # main method part from twint -- https://github.com/twintproject/twint
        response_json = json.loads(response_text)
        if len(response_json['globalObjects']['tweets']) == 0:
            return list()
        feed = []
        for timeline_entry in response_json['timeline']['instructions'][0]['addEntries']['entries']:
            # this will handle the cases when the timeline entry is a tweet
            if timeline_entry['entryId'].startswith('sq-I-t-') or timeline_entry['entryId'].startswith('tweet-'):
                if 'tweet' in timeline_entry['content']['item']['content']:
                    _id = timeline_entry['content']['item']['content']['tweet']['id']
                    # skip the ads
                    if 'promotedMetadata' in timeline_entry['content']['item']['content']['tweet']:
                        continue
                elif 'tombstone' in timeline_entry['content']['item']['content'] and 'tweet' in \
                        timeline_entry['content']['item']['content']['tombstone']:
                    _id = timeline_entry['content']['item']['content']['tombstone']['tweet']['id']
                else:
                    _id = None
                if _id is None:
                    raise ValueError('Unable to find ID of tweet in timeline.')
                try:
                    temp_obj = response_json['globalObjects']['tweets'][_id]
                except KeyError:
                    print('encountered a deleted tweet with id {}'.format(_id))
                    continue
                temp_obj['user_data'] = response_json['globalObjects']['users'][temp_obj['user_id_str']]
                if 'retweeted_status_id_str' in temp_obj:
                    rt_id = temp_obj['retweeted_status_id_str']
                    _dt = response_json['globalObjects']['tweets'][rt_id]['created_at']
                    _dt = datetime.strptime(_dt, '%a %b %d %H:%M:%S %z %Y')
                    _dt = response_json(_dt)
                    _dt = str(_dt.strftime(_Tweet_formats['datetime']))
                    temp_obj['retweet_data'] = {
                        'user_rt_id': response_json['globalObjects']['tweets'][rt_id]['user_id_str'],
                        'user_rt': response_json['globalObjects']['tweets'][rt_id]['full_text'],
                        'retweet_id': rt_id,
                        'retweet_date': _dt,
                    }
                feed.append(TwintBasedTweetParser._tweet_dict_to_tweet_object(temp_obj))
        return feed

    @staticmethod
    def _tweet_dict_to_tweet_object(tweet) -> Tweet:
        return Tweet(
            created_at=tweet['created_at'],
            id_str=tweet['id_str'],
            conversation_id_str=tweet['conversation_id_str'],
            # there was the problem with pandas exporting because \r is old version of \n
            full_text=tweet['full_text'].replace('\r', '\n'),
            lang=tweet['lang'],
            favorited=tweet['favorited'],
            retweeted=tweet['retweeted'],
            retweet_count=tweet['retweet_count'],
            favorite_count=tweet['favorite_count'],
            reply_count=tweet['reply_count'],
            quote_count=tweet['quote_count'],
            quoted_status_id_str=tweet['quoted_status_id_str'] if tweet['is_quote_status'] else '',
            quoted_status_short_url=tweet['quoted_status_permalink']['url'] if tweet['is_quote_status'] else '',
            quoted_status_expand_url=tweet['quoted_status_permalink']['expanded'] if tweet['is_quote_status'] else '',
            user_id_str=tweet['user_data']['id_str'],
            user_name=tweet['user_data']['screen_name'],
            user_full_name=tweet['user_data']['name'],
            user_verified=tweet['user_data']['verified']
        )

    @staticmethod
    def _parse_cursor_first_location(response_json: any) -> Optional[str]:
        try:
            return response_json['timeline']['instructions'][0]['addEntries']['entries'][-1]['content'][
                'operation']['cursor']['value']
        except KeyError:
            return None
        except IndexError:
            return None

    @staticmethod
    def _parse_cursor_second_location(response_json: any) -> Optional[str]:
        try:
            return response_json['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation'][
                'cursor']['value']
        except KeyError:
            return None
        except IndexError:
            return None

    def parse_cursor(self, response_content: str) -> Optional[str]:
        """Method to extract next cursor to scrap request from web response."""
        response_json = json.loads(response_content)
        next_cursor = TwintBasedTweetParser._parse_cursor_first_location(response_json)
        if next_cursor is None:
            next_cursor = TwintBasedTweetParser._parse_cursor_second_location(response_json)
        return next_cursor
