import os
from re import sub
from django.contrib.staticfiles.storage import AppStaticStorage


class NamespacedAngularAppStorage(AppStaticStorage):
    """
    A file system storage backend that takes an app module and works
    for the ``app`` directory of it.  The app module will be included
    in the url for the content.
    """
    source_dir = 'app'

    def __init__(self, app, *args, **kwargs):
        """
        Returns a static file storage if available in the given app.
        """
        # app is the actual app module
        self.prefix = os.path.join(*(app.split('.')))
        super(NamespacedAngularAppStorage, self).__init__(app, *args, **kwargs)

    def path(self, name):
        name = sub('^' + self.prefix + os.sep, '', name)
        return super(NamespacedAngularAppStorage, self).path(name)


class NamespacedE2ETestAppStorage(AppStaticStorage):
    """
    A file system storage backend that takes an app module and works
    for the ``tests/e2e`` directory of it.  The app module will be included
    in the url for the content.  NOTE: This should only be used for
    end-to-end testing.
    """
    source_dir = os.path.join('tests', 'e2e')

    def __init__(self, app, *args, **kwargs):
        """
        Returns a static file storage if available in the given app.
        """
        # app is the actual app module
        prefix_args = [self.source_dir] + app.split('.')
        self.prefix = os.path.join(*prefix_args)
        super(NamespacedE2ETestAppStorage, self).__init__(app, *args, **kwargs)


class NamespacedLibTestAppStorage(AppStaticStorage):
    """
    A file system storage backend that takes an app module and works
    for the ``tests/lib`` directory of it.  The app module will be included
    in the url for the content.  NOTE: This should only be used for
    end-to-end testing.
    """
    source_dir = os.path.join('tests', 'lib')

    def __init__(self, app, *args, **kwargs):
        """
        Returns a static file storage if available in the given app.
        """
        # app is the actual app module
        prefix_args = app.split('.') + ['lib']
        self.prefix = os.path.join(*prefix_args)
        super(NamespacedLibTestAppStorage, self).__init__(app, *args, **kwargs)
