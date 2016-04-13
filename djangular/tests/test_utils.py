import os

from djangular import utils
from django.test import SimpleTestCase


class SiteAndPathUtilsTest(SimpleTestCase):

    site_utils = utils.SiteAndPathUtils()

    def test_djangular_root(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        djangular_dir = os.path.dirname(current_dir)
        self.assertEqual(djangular_dir, self.site_utils.get_djangular_root())
