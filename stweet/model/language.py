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

    ENGLISH = 'en'
    ARABIC = 'ar'
    BASQUE = 'eu'
    BENGALI = 'bn'
    BULGARIAN = 'bg'
    TRADITIONAL_CHINESE = 'zh-tw'
    SIMPLIFIED_CHINESE = 'zh-cn'
    CROATIAN = 'hr'
    CZECH = 'cs'
    DANISH = 'da'
    FINNISH = 'fi'
    FRENCH = 'fr'
    GREEK = 'el'
    GUJARATI = 'gu'
    HEBREW = 'he'
    HINDI = 'hi'
    SPANISH = 'es'
    INDONESIAN = 'id'
    JAPANESE = 'ja'
    CANADIAN = 'kn'
    CATALAN = 'ca'
    KOREAN = 'ko'
    MARATHI = 'mr'
    DUTCH = 'nl'
    GERMAN = 'de'
    NORWEGIAN = 'no'
    PERSIAN = 'fa'
    POLISH = 'pl'
    PORTUGUESE = 'pt'
    RUSSIAN = 'ru'
    ROMANIAN = 'ro'
    SERBIAN = 'sr'
    SLOVAK = 'sk'
    SWEDISH = 'sv'
    THAI = 'th'
    TAMIL = 'ta'
    TURKISH = 'tr'
    UKRAINIAN = 'uk'
    URDU = 'ur'
    HUNGARIAN = 'hu'
    VIETNAMESE = 'vi'
    ITALIAN = 'it'
