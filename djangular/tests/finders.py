import os

from . import base
from djangular import finders
from django.test import TestCase

APP_BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class NamespacedAngularAppDirectoriesFinderTest(TestCase):
    @base.test_with_angularapp_template_as_python_module
    def test_find(self):
        finder = finders.NamespacedAngularAppDirectoriesFinder(apps=['djangular.config.angularapp_template'])
        self.assertEqual(
            finder.find('djangular/config/angularapp_template/index.html'),
            '{0}/config/angularapp_template/app/index.html'.format(APP_BASE_DIR)
        )


class NamespacedE2ETestAppDirectoriesFinderTest(TestCase):
    @base.test_with_angularapp_template_as_python_module
    def test_find(self):
        finder = finders.NamespacedE2ETestAppDirectoriesFinder(apps=['djangular.config.angularapp_template'])
        self.assertEqual(
            finder.find('tests/e2e/djangular/config/angularapp_template/runner.html'),
            '{0}/config/angularapp_template/tests/e2e/runner.html'.format(APP_BASE_DIR)
        )


class NamespacedLibTestAppDirectoriesFinderTest(TestCase):
    @base.test_with_angularapp_template_as_python_module
    def test_find(self):
        finder = finders.NamespacedE2ETestAppDirectoriesFinder(apps=['djangular.config.angularapp_template'])
        self.assertEqual(
            finder.find('tests/e2e/djangular/config/angularapp_template/runner.html'),
            '{0}/config/angularapp_template/tests/e2e/runner.html'.format(APP_BASE_DIR)
        )
