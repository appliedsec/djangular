import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class SiteAndPathUtils(object):
    """
    Mixin to get commonly used directories in Djangular Commands
    """
    def get_default_site_app(self):
        """
        Retrieves the name of the django app that contains the site config.
        """
        return os.environ["DJANGO_SETTINGS_MODULE"].replace('.settings', '')

    def get_default_site_path(self):
        """
        Retrieves the name of the django app that contains the site config.
        """
        settings_module = __import__(self.get_default_site_app())
        return settings_module.__path__[0]

    def get_djangular_root(self):
        """
        Returns the absolute path of the djangular app.
        """
        return CURRENT_DIR

    def get_project_root(self):
        """
        Retrieves the root of the project directory without having to have a entry in the settings.
        """
        default_site = self.get_default_site_app()
        path = self.get_default_site_path()
        # Move up one directory per '.' in site path.  Most sites are at the top level, so this is just a precaution.
        for _ in range(len(default_site.split('.'))):
            path = os.path.dirname(path)
        return path
