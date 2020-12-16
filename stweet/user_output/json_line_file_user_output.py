"""UserOutput which saves users as JSON objects."""

from typing import List

from .user_output import UserOutput
from ..mapper.user_json_mapper import user_to_json
from ..model import User


class JsonLineFileUserOutput(UserOutput):
    """UserOutput which saves users as JSON objects.

    UserOutput which saves user data by request received users batch to text file.
    Every user is saved in one line, this is JSON object.
    """

    file_name: str

    def __init__(self, file_name: str):
        """Creates instance of JsonLineFileUserOutput."""
        self.file_name = file_name

    def export_users(self, users: List[User]):
        """Append new user JSON strings to file."""
        with open(self.file_name, 'a') as file:
            for user in users:
                file.write(f'{user_to_json(user)}\n')
        return
