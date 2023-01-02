import json
from typing import List, Optional

import arrow

from ..model.cursor import Cursor
from ..model.tweet_raw import TweetRaw
from ..model.user_raw import UserRaw


def get_scroll_cursor(instructions: List[any]) -> Optional[Cursor]:
    entries = [
        [entry for entry in instruction['addEntries']['entries']]
        for instruction in instructions if 'addEntries' in instruction
    ]
    entries = [item for sublist in entries for item in sublist]
    replace_entries = [
        instruction['replaceEntry']['entry']
        for instruction in instructions if 'replaceEntry' in instruction
    ]
    entries.extend(replace_entries)
    bottom_entries = [it for it in entries if it['entryId'] == 'cursor-bottom-0']
    bottom_entry = None if len(bottom_entries) == 0 else bottom_entries[0]
    if bottom_entry is not None:
        cursor_raw = bottom_entry['content']['operation']['cursor']
        return Cursor(cursor_raw['cursorType'], cursor_raw['value'])
    else:
        return None


def parse_users(response: str) -> List[UserRaw]:
    users_dict = json.loads(response)['globalObjects']['users']
    return [
        UserRaw(json.dumps(users_dict[it]), arrow.now())
        for it in users_dict.keys()
    ]


def parse_tweets(response: str) -> List[TweetRaw]:
    users_dict = json.loads(response)['globalObjects']['tweets']
    return [
        TweetRaw(json.dumps(users_dict[it]), arrow.now())
        for it in users_dict.keys()
    ]
