import django
import os

from django.test import SimpleTestCase

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _call_test_func(self, test_fn):
    apps = None
    need_to_call_unset = False

    if django.get_version() >= '1.7':
        from django.apps import apps

        if not apps.is_installed('djangular.config.angularseed_template'):
            apps.set_installed_apps(tuple([
                'djangular.config.angularseed_template']))
            need_to_call_unset = True

    try:
        test_fn(self)
    finally:
        if apps and need_to_call_unset:
            apps.unset_installed_apps()


def test_with_angularseed_template_as_django_app(test_fn):
    def fn(self):
        extra_init_py_files = []
        try:
            # Temporarily make the template dirs into python modules by adding
            # the __init__.py files.
            for directory in [
                    'config', os.path.join('config', 'angularseed_template')]:
                current_file_name = os.path.join(
                    BASE_DIR, '..', directory, '__init__.py')
                current_file = open(current_file_name, 'w')
                extra_init_py_files.append(current_file)
                current_file.close()

        except Exception as e:
            self.fail('Could not create files due to {0}'.format(e.message))

        else:
            _call_test_func(self, test_fn)

        finally:
            for py_file in extra_init_py_files:
                if os.path.exists(py_file.name):
                    os.remove(py_file.name)

                compiled_file_name = '{0}c'.format(py_file.name)
                if os.path.exists(compiled_file_name):
                    os.remove(compiled_file_name)

    return fn


class TestAngularSeedAsPythonModuleTest(SimpleTestCase):

    @test_with_angularseed_template_as_django_app
    def test_init_py_created(self):
        self.assertTrue(os.path.exists('{0}/../config/__init__.py'.format(BASE_DIR)))