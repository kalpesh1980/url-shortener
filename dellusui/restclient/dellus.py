"""Dellus REST api client"""
import requests

from restclient.base import Client, catch_connection_error
from restclient.errors import (
    ObjectNotFound, UnAuthorized)
from urllib.parse import urlparse

__all__ = [
    'DellusApiClient'
]

AUTH_COOKIE_NAME = 'access_token'
REFRESH_COOKIE_NAME = 'refresh_token'


class DellusApiClient(Client):
    """Dellus REST API wrapper class"""

    def __init__(self, rest_url, username, password, hostname, request=None):
       
        self.name = username
        self.password = password
        self.rest_url = rest_url
        scheme = 'http://' if not urlparse(hostname).scheme else ''
        self.HOSTNAME = '{}{}'.format(scheme, hostname)
        self.request = request
        self.cookies = None if request is None else request.COOKIES
        super().__init__(rest_url, basic_auth=True, username=username, password=password)

    def __repr__(self):
        return '<DellusApiClient ({0.name}:{0.password}) {0.rest_url}>'.format(
            self)

    @property
    def header(self):
        _header = dict()
        if self.request is None:
            return _header
        if self.cookies and self.cookies.get(AUTH_COOKIE_NAME):
            _header = dict(JWT_Authorization='Bearer {}'.format(
                self.cookies.get(AUTH_COOKIE_NAME)))
        remote_addr = self.request.META.get('REMOTE_ADDR')
        _header['Dellus-App-User-Ip'] = self.request.META.get(
                                            'HTTP_X_REAL_IP', remote_addr)
        _header['Dellus-Http-Rreferrer'] = self.request.META.get('HTTP_REFERER')
        _header['Dellus-Http-User-Agent'] = self.request.META.get(
            'HTTP_USER_AGENT')
        _header['Dellus-Header-Key'] = 'KJ*57*6)(*&^dh'
        return _header

    @property
    def refresh_header(self):
        if self.cookies and self.cookies.get(REFRESH_COOKIE_NAME):
            return dict(JWT_Authorization='Bearer {}'.format(
                self.cookies.get(REFRESH_COOKIE_NAME)))    

    @catch_connection_error
    def ping(self):
        r = requests.get(self.rest_url, headers=self.header)
        if r.status_code // 100 == 2:
            return 'PONG'

    @catch_connection_error
    def shorten(self, long_url, custom_code=None, description=None,
                owner=None, secret=None, expire_after=None):
       
        url_path = '/api/shorten'
        payload = dict(long_url=long_url,
                       short_code=custom_code,
                       is_custom=custom_code is not None and custom_code != '',
                       description=description,
                       is_protected=secret is not None and secret != '',
                       expire_after=expire_after,
                       secret_key=secret,
                       owner=owner)
        r = self.call(url_path, data=payload, return_for_status=401)
        resp = r.json()
        if int(r.status_code) == 401:
            if resp['sub_status'] == 101:
                self.refresh_access_token()
                if self.header is None:
                    raise UnAuthorized('Please login again to continue')
                r = self.call(url_path, data=payload)
                resp = r.json()
        if resp.get('short_url'):
            resp['short_url'] = self.makeurl(self.HOSTNAME, resp['short_code'])
        return resp

    @catch_connection_error
    def get_longurl_data(self, long_url):
       
        url_path = '/api/shorten?url=' + long_url
        r = requests.get(self.rest_url + url_path, headers=self.header)
        if r.status_code // 100 != 2:
            raise ObjectNotFound(r.json())
        return r.json()

    @catch_connection_error
    def unshorten(self, short_url_code, secret=None):
       
        short_code = urlparse(short_url_code).path.strip('/')
        url_path = '/api/unshorten?url=' + self.rest_url + '/' + short_code
        r = self.call(url_path, headers=dict(secret_key=secret))
        resp = r.json()
        if resp.get('short_code'):
            resp['short_url'] = self.makeurl(self.HOSTNAME, resp['short_code'])
        return resp  
