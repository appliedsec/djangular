import os

from django.test import SimpleTestCase

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def test_with_angularapp_template_as_python_module(test_fn):
    def fn(self):
        config_module_file = None
        try:
            # Temporarily make config a python module by adding the __init__.py file.
            config_module_file = open('{0}/../config/__init__.py'.format(BASE_DIR), 'w')
            config_module_file.close()

        except Exception as e:
            self.fail('Could not create files due to {0}'.format(e.message))

        else:
            test_fn(self)

        finally:
            if config_module_file:
                if os.path.exists(config_module_file.name):
                    os.remove(config_module_file.name)

                compiled_file_name = '{0}c'.format(config_module_file.name)
                if os.path.exists(compiled_file_name):
                    os.remove(compiled_file_name)

    return fn


class TestAngularAppAsPythonModuleTest(SimpleTestCase):

    @test_with_angularapp_template_as_python_module
    def test_init_py_created(self):
        self.assertTrue(os.path.exists('{0}/../config/__init__.py'.format(BASE_DIR)))