import json
from datetime import datetime
from typing import List

from stweet.model.tweet import Tweet

_Tweet_formats = {
    'datetime': '%Y-%m-%d %H:%M:%S %Z',
    'datestamp': '%Y-%m-%d',
    'timestamp': '%H:%M:%S'
}


# TODO fix this class -- loaded JSON as class field, try changeł datetime format
class TweetParser:

    @staticmethod
    def parse_tweets(response_text: str) -> List[Tweet]:
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
                feed.append(TweetParser._tweet_dict_to_tweet_object(temp_obj))
        return feed

    @staticmethod
    def _tweet_dict_to_tweet_object(tweet) -> Tweet:
        return Tweet(
            created_at=tweet['created_at'],
            id_str=tweet['id_str'],
            conversation_id_str=tweet['conversation_id_str'],
            full_text=tweet['full_text'],
            lang=tweet['lang'],
            favorited=tweet['favorited'],
            retweeted=tweet['retweeted'],
            retweet_count=tweet['retweet_count'],
            favorite_count=tweet['favorite_count'],
            reply_count=tweet['reply_count'],
            quote_count=tweet['quote_count'],
            user_id_str=tweet['user_data']['id_str'],
            user_name=tweet['user_data']['name'],
            user_full_name=tweet['user_data']['screen_name']
        )

    @staticmethod
    def parse_cursor(response_content: str) -> str:
        response_json = json.loads(response_content)
        try:
            next_cursor = response_json['timeline']['instructions'][0]['addEntries']['entries'][-1]['content'][
                'operation']['cursor']['value']
        except KeyError:
            # this is needed because after the first request location of cursor is changed
            next_cursor = \
                response_json['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation'][
                    'cursor']['value']
        return next_cursor
