"""UserOutput which saves user data by request received users batch to CSV file."""

import os
from typing import List

import pandas as pd

from .user_output import UserOutput
from ..mapper.user_dict_mapper import user_to_flat_dict
from ..model import User

_fields_list = [
    'created_at', 'id_str', 'rest_id_str', 'default_profile', 'default_profile_image', 'description',
    'favourites_count', 'followers_count', 'friends_count', 'has_custom_timelines', 'listed_count', 'location',
    'media_count', 'name', 'pinned_tweet_ids_str', 'profile_banner_url', 'profile_banner_url',
    'profile_image_url_https', 'protected', 'screen_name', 'statuses_count', 'verified'
]


class CsvUserOutput(UserOutput):
    """CsvUserOutput saves user data by request received users batch to CSV file."""

    file_location: str
    add_header_on_start: bool

    def __init__(self, file_location: str, add_header_on_start: bool = True):
        """Create instance of CsvUserOutput."""
        self.file_location = file_location
        self.add_header_on_start = add_header_on_start

    def export_users(self, users: List[User]):
        """Export users to CSV."""
        dict_list = [user_to_flat_dict(it) for it in users]
        df = pd.DataFrame(dict_list, columns=_fields_list)
        df.to_csv(
            path_or_buf=self.file_location,
            mode='a',
            header=self._header_to_add(),
            index=False
        )
        return

    def _header_to_add(self):
        return (not self._file_exists()) or self._file_is_empty()

    def _file_exists(self) -> bool:
        return os.path.isfile(self.file_location)

    def _file_is_empty(self) -> bool:
        return os.stat(self.file_location).st_size == 0
