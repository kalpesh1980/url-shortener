import json
import string
import operator

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django import forms
from django.conf import settings
from utils import dellus_client_object
from restclient.errors import ObjectNotFound, UnAuthorized, LinkExpired, \
    InvalidInput
from restclient.error_msg import API_ERROR, INVALID_TOKEN

# TODO: [IMP] dellusui to return 500 page when internal error occurs.
AUTH_COOKIE_NAME = settings.AUTH_COOKIE_NAME
MAX_SHORT_CODE_LEN = 8
INVALID_CUSTOM_CODE_ERROR = ("Invalid value. Length should be <= 8 and should"
                             " be a valid alphabat, digit or a mix of both")
VALID_INPUT_CHARS = string.ascii_letters + string.digits


class URLForm(forms.Form):
    long_url = forms.URLField(help_text='Long Link To Shorten',
                              label='Long URL')
    custom_url = forms.CharField(required=False, label='Custom URL')
    remember_time = forms.IntegerField(required=False,
                                       label='Link Expire Time')
    remember_check = forms.BooleanField(required=False)
    secret_key = forms.CharField(required=False, label='Secret Key')
    secret_check = forms.BooleanField(required=False)    

def link_shortener(request):
    dellus_client = dellus_client_object(settings, request)
    if request.method == 'POST':
        form = URLForm(request.POST)
        context = dict(form=form)
        if form.is_valid():
            try:
                resp = dellus_client.shorten(
                    long_url=form.cleaned_data['long_url'],
                    custom_code=form.cleaned_data['custom_url'],
                    secret=form.cleaned_data['secret_key'],
                    expire_after=form.cleaned_data['remember_time']
                )
            except (ObjectNotFound, InvalidInput) as e:
                return render(request, '400.html',
                              context=API_ERROR(e.args[0]), status=400)
            short_code = resp['short_code']
        else:
            return render(
                request, "invalid_form.html", context=context, status=400)
        return redirect('get_short_link', code=short_code)

    if request.method == 'GET':
        return render(request, '400.html', status=400)


def get_short_link(request, code):   
    if request.method == 'GET':
        try:          
            schema = 'https://' if request.is_secure() else 'http://'
            url_obj = {}
            url_obj['short_url'] = (
                schema + request.META['HTTP_HOST'] + '/' + url_obj.get(
                    'short_code', code)
            )
        except ObjectNotFound as e:
            return render(request, '404.html',
                          context=API_ERROR(e.args[0]), status=404)
        context = dict(short_url=url_obj['short_url'], short_code=code)
        return render(request, 'dellus/short_url.html', context=context)
    return render(request, '400.html', status=400)


def link_unshorten(request, code):
    dellus_client = dellus_client_object(settings, request)
    if request.method == 'GET':
        try:
            url_obj = dellus_client.unshorten(code)
        except UnAuthorized:
            return redirect('/link/secret?next={}'.format(code))
        except (LinkExpired, ObjectNotFound) as e:
            return render(request, '404.html',
                          context=API_ERROR(e.args[0]), status=404)
        long_url = url_obj['long_url']
        return redirect(long_url, permanent=True)

def index(request):
    """Index page"""
    response = render(request, 'dellus/index.html')
    if (request.COOKIES.get(AUTH_COOKIE_NAME) and
            request.COOKIES.get('refresh_token')):
        dellus_client = dellus_client_object(settings, request)
        access_token = dellus_client.refresh_access_token()
        response.set_cookie(
            AUTH_COOKIE_NAME, access_token.get(AUTH_COOKIE_NAME))
    return response
