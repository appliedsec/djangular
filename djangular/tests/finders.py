import django
import os

from . import base
from djangular import finders
from django.test import TestCase

APP_BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class NamespacedAngularAppDirectoriesFinderTest(TestCase):
    @base.test_with_angularapp_template_as_django_app
    def test_find(self):
        if django.get_version() >= '1.7':
            finder = finders.NamespacedAngularAppDirectoriesFinder(
                app_names=['djangular.config.angularapp_template'])
        else:
            finder = finders.NamespacedAngularAppDirectoriesFinder(
                apps=['djangular.config.angularapp_template'])

        self.assertEqual(
            finder.find('djangular/config/angularapp_template/index.html'),
            '{0}/config/angularapp_template/angular/index.html'.format(
                APP_BASE_DIR)
        )


class NamespacedE2ETestAppDirectoriesFinderTest(TestCase):
    @base.test_with_angularapp_template_as_django_app
    def test_find(self):
        if django.get_version() >= '1.7':
            finder = finders.NamespacedE2ETestAppDirectoriesFinder(
                app_names=['djangular.config.angularapp_template'])
        else:
            finder = finders.NamespacedE2ETestAppDirectoriesFinder(
                apps=['djangular.config.angularapp_template'])

        self.assertEqual(
            finder.find(
                'tests/e2e/djangular/config/angularapp_template/runner.html'),
            '{0}/config/angularapp_template/tests/e2e/runner.html'.format(
                APP_BASE_DIR)
        )
