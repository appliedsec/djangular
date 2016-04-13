import django
import os

from djangular.tests.test_base import test_with_angularseed_template_as_django_app
from djangular import finders
from django.test import SimpleTestCase

APP_BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class NamespacedAngularAppDirectoriesFinderTest(SimpleTestCase):
    @test_with_angularseed_template_as_django_app
    def test_find(self):
        if django.get_version() >= '1.7':
            finder = finders.NamespacedAngularAppDirectoriesFinder(
                app_names=['djangular.config.angularseed_template'])
        else:
            finder = finders.NamespacedAngularAppDirectoriesFinder(
                apps=['djangular.config.angularseed_template'])

        self.assertEqual(
            finder.find('djangular/config/angularseed_template/index.html'),
            '{0}/config/angularseed_template/angular/index.html'.format(
                APP_BASE_DIR)
        )


class NamespacedE2ETestAppDirectoriesFinderTest(SimpleTestCase):

    @test_with_angularseed_template_as_django_app
    def test_find(self):
        self.skipTest('E2E Testing is not implemented yet...')

        if django.get_version() >= '1.7':
            finder = finders.NamespacedE2ETestAppDirectoriesFinder(
                app_names=['djangular.config.angularseed_template'])
        else:
            finder = finders.NamespacedE2ETestAppDirectoriesFinder(
                apps=['djangular.config.angularseed_template'])

        self.assertEqual(
            finder.find(
                'tests/e2e/djangular/config/angularseed_template/runner.html'),
            '{0}/config/angularseed_template/tests/e2e/runner.html'.format(
                APP_BASE_DIR)
        )
