import django

if django.get_version() < '1.7':
    from djangular import storage
    from django.test import SimpleTestCase

    from . import base

    class NamespacedAppAngularStorageTest(SimpleTestCase):
        def test_source_dir_is_angular(self):
            self.assertEqual(storage.NamespacedAngularAppStorage.source_dir, 'angular')

        def test_prefix_is_given_app_name(self):
            app_storage = storage.NamespacedAngularAppStorage('djangular')
            self.assertEqual(app_storage.prefix, 'djangular')

        @base.test_with_angularapp_template_as_django_app
        def test_prefix_is_given_app_name_for_more_complicated_scenario(self):
            app_storage = storage.NamespacedAngularAppStorage('djangular.config.angularapp_template')
            self.assertEqual(app_storage.prefix, 'djangular/config/angularapp_template')


    class NamespacedE2ETestAppStorageTest(SimpleTestCase):
        def test_source_dir_is_tests(self):
            self.assertEqual(storage.NamespacedE2ETestAppStorage.source_dir, 'tests/e2e')

        def test_prefix_is_given_app_name(self):
            app_storage = storage.NamespacedE2ETestAppStorage('djangular')
            self.assertEqual(app_storage.prefix, 'tests/e2e/djangular')

        @base.test_with_angularapp_template_as_django_app
        def test_prefix_is_given_app_name_for_more_complicated_scenario(self):
            app_storage = storage.NamespacedE2ETestAppStorage('djangular.config.angularapp_template')
            self.assertEqual(app_storage.prefix, 'tests/e2e/djangular/config/angularapp_template')