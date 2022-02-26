"""Fetch info from the short url click"""
import geoip2.database

def parse_request(request):
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    data = dict(
        referrer=request.referrer,
        user_agent=request.headers.get("User-Agent")
    )
    return data


def parse_header(request):
   
    ip = request.headers.get('Dellus-App-User-Ip')
    data = dict(
        referrer=request.headers.get('Dellus-Http-Rreferrer'),
        user_agent=request.headers.get('Dellus-Http-User-Agent')
    )
    return data