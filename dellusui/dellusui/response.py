from django.conf import settings


class ResponseDellusui:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        response.set_cookie(
            settings.AUTH_COOKIE_NAME, request.COOKIES['access_token'])
        return response

