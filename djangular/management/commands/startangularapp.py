import django
import os

from django.core import management as mgmt
from django.core.management.templates import TemplateCommand
from djangular import utils


class Command(utils.SiteAndPathUtils, TemplateCommand):
    help = ("Creates a Djangular app directory structure for the given app "
            "name in the current directory or optionally in the given "
            "directory.")

    if django.get_version() > "1.7":
        requires_system_checks = False
    else:
        requires_model_validation = False

    def handle(self, app_name=None, target=None, **options):
        mgmt.call_command('startapp', app_name, target, **options)

        # Override the options to setup the template command.
        options.update({
            'template': os.path.join(
                self.get_djangular_root(), 'config', 'angularseed_template'),
            'extensions': ['.html', '.js'],  # Parse HTML And JS files
            'files': ['app.css']
        })

        super(Command, self).handle(
            'app', app_name, target or app_name, **options)

