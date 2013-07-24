import os

from djangular import utils
from django.core.management import base, templates


class Command(utils.SiteAndPathUtils, templates.TemplateCommand):
    help = ("Augments a Django site directory with needed Djangular files "
            "for the given site name in the current directory.")
    args = '[site]'
    option_list = base.BaseCommand.option_list

    def handle(self, site_name=None, target=None, *args, **options):
        if site_name is None:
            site_name = self.get_default_site_app()

        # Include djangular_root variable in the template and setup the rest as if the other options existed.
        options.update({
            'djangular_root': self.get_djangular_root(),
            'template': os.path.join(self.get_djangular_root(), 'config', 'angularsite_template'),
            'extensions': [],
            'files': []
        })

        # Override target with site_name, so that we won't get directory already exists errors.
        super(Command, self).handle('site', name=site_name, target=site_name, **options)

        template_path = os.path.join(site_name, 'templates')
        self.stdout.write(
            'Update the Karma config templates in %s to add any additional JS dependencies.' % template_path)

