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
        self.prefix = app
        super(NamespacedAngularAppStorage, self).__init__(app, *args, **kwargs)

class NamespacedE2ETestAppStorage(AppStaticStorage):
    """
    A file system storage backend that takes an app module and works
    for the ``tests/e2e`` directory of it.  The app module will be included
    in the url for the content.  NOTE: This should only be used for
    end-to-end testing.
    """
    source_dir = 'tests/e2e'

    def __init__(self, app, *args, **kwargs):
        """
        Returns a static file storage if available in the given app.
        """
        # app is the actual app module
        self.prefix = '{0}/{1}'.format(self.source_dir, app)
        super(NamespacedE2ETestAppStorage, self).__init__(app, *args, **kwargs)


class NamespacedLibTestAppStorage(AppStaticStorage):
    """
    A file system storage backend that takes an app module and works
    for the ``tests/lib`` directory of it.  The app module will be included
    in the url for the content.  NOTE: This should only be used for
    end-to-end testing.
    """
    source_dir = 'tests/lib'

    def __init__(self, app, *args, **kwargs):
        """
        Returns a static file storage if available in the given app.
        """
        # app is the actual app module
        self.prefix = '{0}/lib'.format(app)
        super(NamespacedLibTestAppStorage, self).__init__(app, *args, **kwargs)
