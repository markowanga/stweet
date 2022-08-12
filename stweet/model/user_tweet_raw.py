from arrow import Arrow

from stweet.model.raw_data import RawData


class UserTweetRaw(RawData):
    def __init__(self, raw_value: str, download_datetime: Arrow):
        super().__init__('UserTweetRaw', raw_value, download_datetime)
