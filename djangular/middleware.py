
class AngularJsonVulnerabilityMiddleware(object):
    """
    A middleware that inserts the AngularJS JSON Vulnerability request on JSON responses.
    """
    # The AngularJS JSON Vulnerability content prefix. See http://docs.angularjs.org/api/ng.$http
    CONTENT_PREFIX = b")]}',\n"

    # Make this class easy to extend by allowing class level access.
    VALID_STATUS_CODES = [200, 201, 202]
    VALID_CONTENT_TYPES = ['application/json']

    def process_response(self, request, response):
        if response.status_code in self.VALID_STATUS_CODES and response['Content-Type'] in self.VALID_CONTENT_TYPES:
            response.content = self.CONTENT_PREFIX + response.content

        return response