"""Methods to read users from files."""

from typing import List

import pandas as pd

from ..mapper.user_dict_mapper import create_user_from_flat_dict
from ..mapper.user_json_mapper import create_user_from_json
from ..model import User


def read_users_from_csv_file(file_path: str) -> List[User]:
    """Method to read tweets from csv file."""
    df = pd.read_csv(file_path, dtype={
        'pinned_tweet_ids_str': str,
        'profile_banner_url': str,
        'location': str,
        'description': str
    })
    df.pinned_tweet_ids_str.fillna('', inplace=True)
    df.profile_banner_url.fillna('', inplace=True)
    df.location.fillna('', inplace=True)
    df.description.fillna('', inplace=True)
    return [create_user_from_flat_dict(row) for _, row in df.iterrows()]


def read_users_from_json_lines_file(file_path: str) -> List[User]:
    """Method to read tweets from csv file."""
    file = open(file_path, 'r')
    return [create_user_from_json(line) for line in file.readlines()]
