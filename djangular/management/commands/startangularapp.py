import os

from django.core import management as mgmt
from django.core.management.commands import startapp
from djangular import utils


class Command(utils.SiteAndPathUtils, mgmt.base.BaseCommand):
    help = ("Creates a Djangular app directory structure for the given app "
            "name in the current directory or optionally in the given directory.")
    args = startapp.Command.args
    requires_model_validation = False

    def handle(self, app_name=None, target=None, **options):
        options['template'] = os.path.join(self.get_djangular_root(), 'config', 'angularapp_template')
        options['extensions'] = ['.py', '.js']  # Include JS Files for parsing.
        options['files'] = ['index.html']
        mgmt.call_command('startapp', app_name, target, **options)
