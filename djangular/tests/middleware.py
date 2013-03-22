from djangular import middleware

from django.test import TestCase
from django.http import request, response

class AngularJsonVulnerabilityMiddlewareTest(TestCase):

    def test_that_middleware_does_nothing_to_html_requests(self):
        resp = response.HttpResponse(mimetype='text/html', content='<html></html>')
        mware = middleware.AngularJsonVulnerabilityMiddleware()
        mware.process_response(request.HttpRequest(), resp)

        self.assertEqual(resp.content, '<html></html>')

    def test_that_middleware_does_nothing_to_js_requests(self):
        resp = response.HttpResponse(mimetype='text/javascript', content='var blah = [];')
        mware = middleware.AngularJsonVulnerabilityMiddleware()
        mware.process_response(request.HttpRequest(), resp)

        self.assertEqual(resp.content, 'var blah = [];')

    def test_that_middleware_does_nothing_to_invalid_json_requests(self):
        resp = response.HttpResponse(mimetype='application/json', content='[1, 2, 3]', status=400)
        mware = middleware.AngularJsonVulnerabilityMiddleware()
        mware.process_response(request.HttpRequest(), resp)

        self.assertEqual(resp.content, '[1, 2, 3]')

    def test_that_middleware_adds_prefix_to_valid_json_requests(self):
        resp = response.HttpResponse(mimetype='application/json', content='[1, 2, 3]')
        mware = middleware.AngularJsonVulnerabilityMiddleware()
        mware.process_response(request.HttpRequest(), resp)

        self.assertEqual(resp.content, mware.CONTENT_PREFIX + '[1, 2, 3]')
