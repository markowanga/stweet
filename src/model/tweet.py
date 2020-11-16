import json
from dataclasses import dataclass


@dataclass
class Tweet:
    created_at: str
    id_str: str
    conversation_id_str: str
    full_text: str
    lang: str
    favorited: bool
    retweeted: bool
    retweet_count: int
    favorite_count: int
    reply_count: int
    quote_count: int
    user_id_str: str
    user_name: str
    user_full_name: str

    def to_json_string(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)
