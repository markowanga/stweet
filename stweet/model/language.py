"""Domain Language enum class."""

import enum


class Language(enum.Enum):
    """Domain Language enum class."""

    def __new__(cls, *args, **kwargs):
        """Class __new__ method."""
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, short_value):
        """Class constructor method."""
        self.short_value = short_value

    POLISH = 'pl'
    ENGLISH = 'en'
