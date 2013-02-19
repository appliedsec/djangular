from django.core import management as mgmt
from django.core.management.commands import runserver

class Command(mgmt.base.BaseCommand):
    help = "Starts a lightweight server for end-to-end testing."
    args = runserver.Command.args

    def handle(self, addrport=runserver.DEFAULT_PORT, *args, **options):
        # Hack on the test directories so that the e2e tests can be run.
        from django.conf import settings
        # TODO: Figure out why this prints twice...
        self.stdout.write("Patching settings to include end-to-end test directories...\n")
        new_finders = ['djangular.finders.NamespacedE2ETestAppDirectoriesFinder',
                       'djangular.finders.NamespacedLibTestAppDirectoriesFinder']
        new_finders.extend(settings.STATICFILES_FINDERS)
        settings.STATICFILES_FINDERS = tuple(new_finders)

        # Add port to arguments
        new_args = [addrport]
        new_args.extend(args)
        mgmt.call_command('runserver', *new_args, **options)
