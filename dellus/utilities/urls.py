import re

from dellus.config import config
from urllib.parse import urljoin, urlparse


def validate_url(url):
    """Simple URL validator."""
    url = url or 'invalid'
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    is_valid = regex.match(url) is not None
   
    return is_valid


def make_short_url(short_path):
    short_url = urljoin('{}{}'.format(config.dellus['short_url_schema'], config.dellus['short_url']), short_path)
    return short_url


def get_short_path(short_url):
    parts = urlparse(short_url)
    short_path = parts.path.lstrip('/')
    return short_path
