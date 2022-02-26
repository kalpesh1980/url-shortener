"""A common util file to use methods across different django apps"""
import os
import logging

from restclient.dellus import DellusApiClient

from urllib.parse import urlparse


def make_url(url_address):
    parsed = urlparse(url_address)
    scheme = 'http://' if not parsed.scheme else ''
    return '{}{}'.format(scheme, url_address)


def dellus_client_object(config, request):
    rest_user = config.DELLUS_API_USER
    rest_pass = config.DELLUS_API_PASSWORD
    dellus_api_host, dellus_api_port = urlparse(config.DELLUS_API_ADDRESS).netloc.split(':')

    # Check if DELLUS_API_ADDRESS enviornment varibale is set
    if os.environ.get('DELLUS_API_ADDRESS'):
        dellus_api_host = os.environ.get('DELLUS_API_ADDRESS')
        logging.info('Using environment variable DELLUS_API_ADDRESS. API URL: %s', dellus_api_host)

    rest_url = make_url('http://{}:{}'.format(dellus_api_host, dellus_api_port))
    hostname = config.HOSTNAME
    return DellusApiClient(rest_url, rest_user, rest_pass, hostname, request)
