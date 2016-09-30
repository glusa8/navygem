from django.http import HttpResponse
from django.utils.cache import patch_vary_headers
from navygem.settings import ENV

# TODO(edit)
ACCESS_CONTROL_ALLOW_ORIGIN = 'http://localhost:3000'
ACCESS_CONTROL_ALLOW_METHODS = ['POST', 'OPTIONS']
ACCESS_CONTROL_ALLOW_HEADERS = ['X-CSRFToken', 'Content-Type']
ACCESS_CONTROL_ALLOW_CREDENTIALS = 'true'


class CORSMiddleware(object):
    '''
    This middelware allows for cross-origin resource sharing in DEV environment
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def set_preflight_response_headers(self, response):
        response['Access-Control-Allow-Origin'] = ACCESS_CONTROL_ALLOW_ORIGIN
        response['Access-Control-Allow-Methods'] = ','.join(ACCESS_CONTROL_ALLOW_METHODS)
        response['Access-Control-Allow-Headers'] = ','.join(ACCESS_CONTROL_ALLOW_HEADERS)
        response['Access-Control-Allow-Credentials'] = ACCESS_CONTROL_ALLOW_CREDENTIALS
        patch_vary_headers(response, ['Origin'])

    def set_cors_response_headers(self, response):
        response['Access-Control-Allow-Origin'] = ACCESS_CONTROL_ALLOW_ORIGIN
        response['Access-Control-Allow-Credentials'] = ACCESS_CONTROL_ALLOW_CREDENTIALS
        patch_vary_headers(response, ['Origin'])

    def __call__(self, request):
        if ENV == 'DEV':
            if request.META.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD') == 'POST':
                if request.method == 'OPTIONS':
                    response = HttpResponse()
                    self.set_preflight_response_headers(response)
                    return response

            if request.method == 'POST' and request.path == '/graphql':
                response = self.get_response(request)
                self.set_cors_response_headers(response)
                return response

        return self.get_response(request)
