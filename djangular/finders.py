import django

from django.contrib.staticfiles import finders as s_finders

if django.get_version() >= '1.7':
    import os
    import re

    class NamespacedAngularAppDirectoriesFinder(s_finders.AppDirectoriesFinder):
        """
        A static files finder that looks in the directory of each app as
        specified in the source_dir attribute.
        """
        source_dir = 'angular'

        def __init__(self, app_names=None, *args, **kwargs):
            super(NamespacedAngularAppDirectoriesFinder, self).__init__(
                app_names, *args, **kwargs)

            for app_name, storage in self.storages.iteritems():
                storage.prefix = os.path.join(*(app_name.split('.')))

        def find_in_app(self, app, path):
            app_re = '^{}{}'.format(os.path.join(*(app.split('.'))), os.sep)
            return super(NamespacedAngularAppDirectoriesFinder, self).find_in_app(
                app, re.sub(app_re, '', path)
            )

    # TODO: Still need to convert test finders...
else:
    from . import storage

    class NamespacedAngularAppDirectoriesFinder(s_finders.AppDirectoriesFinder):
        """
        A static files finder that looks in the app directory of each app.
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