import json

import arrow

from stweet.model.user_raw import UserRaw


def parse_user(response_content: str) -> UserRaw:
    return UserRaw(json.dumps(json.loads(response_content)['data']['user']['result']), arrow.now())
