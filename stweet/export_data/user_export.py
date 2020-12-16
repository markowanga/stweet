"""Methods to export_data users."""
from typing import List

from .util import clear_file
from ..model import User
from ..user_output import CsvUserOutput, JsonLineFileUserOutput


def export_users_to_csv(users: List[User], filename: str):
    """Method to export_data users to csv."""
    clear_file(filename)
    CsvUserOutput(filename).export_users(users)
    return


def export_users_to_json_lines(users: List[User], filename: str):
    """Method to export_data users to json lines."""
    clear_file(filename)
    JsonLineFileUserOutput(filename).export_users(users)
    return
