from dellus.exception.error import DellusExcpetion


class URLAuthFailed(DellusExcpetion):
    """Secret key is invalid or not present."""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "Invalid/missing secret key for protected url"
