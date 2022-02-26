"""All invalid/not found like url specific errors go here"""

from dellus.exception.error import DellusExcpetion


class URLNotFound(DellusExcpetion):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def __str__(self):
        return '{0} url not found'.format(self.url)
