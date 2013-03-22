from djangular.management.base import TestacularStartCommand


class Command(TestacularStartCommand):
    help = ("Convenience command to run the Testacular e2e tests in all apps.")
    testacular_config_file = 'testacular-e2e.conf.js'

