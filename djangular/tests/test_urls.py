from django.core.urlresolvers import reverse
from django.test import TestCase


class UrlsTests(TestCase):
    def test_urls_import(self):
        """Smoke test to make sure urls imports are valid."""
        self.assertEqual('/app.js', reverse('djangular-module'))
