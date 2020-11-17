import enum


class Language(enum.Enum):

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, short_value):
        self.short_value = short_value

    POLISH = 'pl'
    ENGLISH = 'en'
