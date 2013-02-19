from . import TestacularStartCommand

class Command(TestacularStartCommand):
    help = ("Convenience command to run the Testacular unit tests in all apps.")
    testacular_config_file = 'testacular.conf.js'

