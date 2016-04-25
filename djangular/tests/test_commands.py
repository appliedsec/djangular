import os
import shutil

from django.test import TestCase
from django.utils._os import upath

from djangular.management.commands.startangularapp import Command as StartAngularAppCommand


class StartAngularAppCommandTests(TestCase):
    def setUp(self):
        # Clean up app directory that is created
        test_dir = os.path.abspath(os.path.dirname(upath(__file__)))
        demo_app_path = os.path.join(test_dir, '../../demo')
        self.addCleanup(shutil.rmtree, demo_app_path)

    def test_runs(self):
        StartAngularAppCommand().handle('demo', verbosity=1)
