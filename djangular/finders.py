import django
from django.contrib.staticfiles import finders as s_finders

# Django rewrote the staticfiles storage internals in 1.7, so...
if django.get_version() >= '1.7':
    import os
    import re

    class NamespacedAppDirectoriesFinder(s_finders.AppDirectoriesFinder):
        """
        A namedspace static files finder that looks in the angular directory of
        each app as specified in the source_dir attribute.
        """
        prepend_source_dir = False

        def __init__(self, app_names=None, *args, **kwargs):
            super(NamespacedAppDirectoriesFinder, self).__init__(
                app_names, *args, **kwargs)

            for app_name, storage in self.storages.items():
                storage.prefix = os.path.join(*(app_name.split('.')))

        def find_in_app(self, app, path):
            if self.prepend_source_dir:
                prefixed_path = os.path.join(self.source_dir, *(app.split('.')))
            else:
                prefixed_path = os.path.join(*(app.split('.')))

            app_re = '^{}{}'.format(prefixed_path, os.sep)
            if re.match(app_re, path):
                return super(NamespacedAppDirectoriesFinder, self).find_in_app(
                    app, re.sub(app_re, '', path)
                )

    class NamespacedAngularAppDirectoriesFinder(NamespacedAppDirectoriesFinder):
        """
        A static files finder that looks in the angular directory of each app.
        """
        source_dir = 'angular'

    class NamespacedE2ETestAppDirectoriesFinder(NamespacedAppDirectoriesFinder):
        """
        A static files finder that looks in the tests/e2e directory of each app.
        """
        source_dir = os.path.join('tests', 'e2e')
        prepend_source_dir = True

else:
    from . import storage

    class NamespacedAngularAppDirectoriesFinder(s_finders.AppDirectoriesFinder):
        """
        A static files finder that looks in the angular directory of each app.
        """
        storage_class = storage.NamespacedAngularAppStorage

    class NamespacedE2ETestAppDirectoriesFinder(s_finders.AppDirectoriesFinder):
        """
        A static files finder that looks in the tests/e2e directory of each app.
        """
        storage_class = storage.NamespacedE2ETestAppStorage

    class NamespacedLibTestAppDirectoriesFinder(s_finders.AppDirectoriesFinder):
        """
        A static files finder that looks in the tests/lib directory of each app.
        """
        storage_class = storage.NamespacedLibTestAppStorage