from navygem.settings import AJAX_SALT
from django.utils.cache import patch_vary_headers
from django.utils.crypto import constant_time_compare
from django.http import HttpResponseForbidden
import hashlib

from navygem.settings import ENV

HTTP_COOKIE_NAME = 'HTTP_COOKIE'

AJAX_TOKEN_COOKIE_NAME = 'ajaxtoken'
AJAX_TOKEN_HEADER_NAME = 'HTTP_X_AJAXTOKEN'
AJAX_URL_PREFIX = '/api'

class AjaxTokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        user = request.user

        if request.path.startswith(AJAX_URL_PREFIX):
            ajax_token_from_session = request.session.get('ajax_token')
            ajax_token_from_cookie = request.META.get(AJAX_TOKEN_HEADER_NAME)

            if ENV == 'DEV':
                cookies = [
                    c.strip()
                    for c
                    in request.META.get(HTTP_COOKIE_NAME).split(';')
                ]
                for c in cookies:
                    if c.startswith(AJAX_TOKEN_COOKIE_NAME):
                        ajax_token_from_cookie = c.split('=')[1]


            if ajax_token_from_session is None:
                if not user.is_authenticated():
                    return HttpResponseForbidden('Please log in.')

                request.session['ajax_token'] = generate_token(user)
                ajax_token_from_session = request.session.get('ajax_token')

            if ajax_token_from_cookie is None:
                return HttpResponseForbidden('AJAX token is missing.')

            if not constant_time_compare(ajax_token_from_session, ajax_token_from_cookie):
                return HttpResponseForbidden('AJAX token is incorrect.')


        response = self.get_response(request)

        # Process response
        if user.is_authenticated():
            response.set_cookie(
                AJAX_TOKEN_COOKIE_NAME,
                generate_token(request.user),
                max_age=60 * 60 * 24 * 365,
                secure=(ENV == 'PROD'),
                httponly=False
            )

            patch_vary_headers(response, ['Cookie'])

        return response

def generate_token(user):
    return hashlib.sha256(
        '{}{}{}'.format(
            AJAX_SALT,
            str(user.last_login),
            user.id
        )
    ).hexdigest()
