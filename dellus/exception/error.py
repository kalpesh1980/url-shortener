
class DellusExcpetion(Exception):
    """Dellus base custom exception class."""


class LinkExpired(DellusExcpetion):
    """Dellus base custom exception class."""


class LinkInvalid(DellusExcpetion):
    """Raised in case an invalid link is passed"""


class ShortURLUnavailable(DellusExcpetion):
    """Raised when a short url already exists and a new insert comes with same
    short url."""
