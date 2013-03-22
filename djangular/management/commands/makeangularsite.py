import os

from djangular.utils import SiteAndPathUtils
from django.core.management.templates import TemplateCommand


class Command(SiteAndPathUtils, TemplateCommand):
    help = ("Augments a Django site directory with needed Djangular files "
            "for the given site name in the current directory.")

    def handle(self, site_name=None, target=None, *args, **options):
        if site_name is None:
            site_name = self.get_default_site_app()

        options['files'] = ['testacular.conf.js', 'testacular-e2e.conf.js']  # Parse Testacular config files.
        options['template'] = os.path.join(self.get_djangular_root(), 'config', 'angularsite_template')
        # Include djangular_root variable in the template.
        options['djangular_root'] = self.get_djangular_root()

        # Override target with site_name, so that we won't get directory already exists errors.
        super(Command, self).handle('site', name=site_name, target=site_name, **options)
