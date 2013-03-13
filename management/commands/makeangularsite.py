from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand

from djangular.management.commands import DefaultSiteMixin

class Command(DefaultSiteMixin, TemplateCommand):
    help = ("Augments a Django site directory with needed Djangular files "
            "for the given site name in the current directory.")

    def handle(self, site_name=None, target=None, *args, **options):
        if site_name is None:
            site_name = self._get_default_site()

        options['files'] = ['testacular.conf.js', 'testacular-e2e.conf.js']  # Parse Testacular config files.
        options['template'] = 'djangular/config/angularsite_template'

        # Override target with site_name, so that we won't get directory already exists errors.
        super(Command, self).handle('site', name=site_name, target=site_name, **options)
