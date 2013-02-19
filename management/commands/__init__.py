import os, subprocess, sys

from optparse import make_option
from django.core.management import base

def _convert_testacular_start_help_options():
    """
    Convert the testacular start help text to make_option entries.
    """
    testacular_help_text = subprocess.check_output(['testacular', 'start', '--help']).split('\n')
    options_start = testacular_help_text.index('Options:') + 1

    return [
    make_option(line.pop(0), help=' '.join(line),
                # Show value=VALUE in the help for options that need a value associated with them.
                action='store' if line[0] in ['<integer>', 'List', '<disable'] else 'store_true'
    )
    for line in [line.split() for line in testacular_help_text[options_start:] if line]
    if line[0] not in ('--version', '--help')  # don't use these, as they are already present
    ]


class TestacularStartCommand(base.BaseCommand):
    """
    A base command that calls testacular from the command line, passing the options and arguments directly.
    """
    testacular_config_file = 'specify in implementing class'
    option_list = _convert_testacular_start_help_options()

    def run_from_argv(self, argv):
        """
        Override the default run_from_argv because we just want to pass the command line args to Testacular.
        """
        stdout = base.OutputWrapper(sys.stdout)

        stdout.write("\n")
        stdout.write("Starting Testacular Server (http://vojtajina.github.com/testacular)\n")
        stdout.write("-------------------------------------------------------------------\n")

        # Move up two directories to the root of the djangular app
        root_app_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        config_file = os.path.join(root_app_path, 'config', self.testacular_config_file)

        # Add testacular command and use argv from the command line
        args = ['testacular', 'start', config_file]
        args.extend(argv[2:])
        os.execvp('testacular', args)

