from . import storage
from django.contrib.staticfiles import finders


class NamespacedAngularAppDirectoriesFinder(finders.AppDirectoriesFinder):
    """
    A static files finder that looks in the app directory of each app.
    """
    storage_class = storage.NamespacedAngularAppStorage


class NamespacedE2ETestAppDirectoriesFinder(finders.AppDirectoriesFinder):
    """
    A static files finder that looks in the tests/e2e directory of each app.
    """
    storage_class = storage.NamespacedE2ETestAppStorage


class NamespacedLibTestAppDirectoriesFinder(finders.AppDirectoriesFinder):
    """
    A static files finder that looks in the tests/lib directory of each app.
    """
    storage_class = storage.NamespacedLibTestAppStorage