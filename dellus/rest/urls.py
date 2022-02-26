from dellus.rest.shorturl import (
    LongUrlApi, ShortURLApi, resolve, dummy, link_stats)
from dellus.rest.manage import app

ONLY_GET = ['GET']
GET_POST = ['GET', 'POST']
ONLY_POST = ['POST']

app.add_url_rule(
    '/api/shorten', view_func=LongUrlApi.as_view('long_url'), methods=GET_POST)
app.add_url_rule(
    '/api/unshorten', view_func=ShortURLApi.as_view('short_url'),
    methods=GET_POST)
    
# This should be last
app.add_url_rule('/<code>', view_func=resolve, methods=ONLY_GET)
