import os
import re
import subprocess
import tempfile

from django import template
from django.core import management as mgmt
from django.conf import settings
from djangular import utils
from optparse import make_option


class Command(utils.SiteAndPathUtils, mgmt.base.BaseCommand):
    """
    A base command that calls Karma from the command line, passing the options and arguments directly.
    """
    help = ("Runs the JS Karma tests for the given test type and apps.  If no apps are specified, tests will be "
            "run for every app in INSTALLED_APPS.")
    args = '[type] [appname ...]'
    option_list = mgmt.base.BaseCommand.option_list + (
        make_option('--greedy', action='store_true',
                    help="Run every app in the project, ignoring passed in apps and the INSTALLED_APPS setting.  "
                         "Note that running e2e tests for non-installed apps will most likely cause them to fail."),
    )
    requires_model_validation = False

    default_test_type = 'unit'
    template_dir = 'templates'

    def get_existing_apps_from(self, app_list):
        """
        Retrieves the apps from the given app_list that exist on the file system.
        """
        project_root = self.get_project_root()
        existing_paths = []

        for app_name in app_list:
            app_name_components = app_name.split('.')
            app_path = os.path.join(*app_name_components)
            full_app_path = os.path.join(project_root, app_path)
            if os.path.exists(full_app_path):
                existing_paths.append(app_path)

        if self.verbosity >= 2:
            self.stdout.write("Running %s tests from apps: %s" % (self.test_type, ', '.join(existing_paths)))
        return existing_paths

    def usage(self, subcommand):
        # Default message when templates are missing
        types_message = mgmt.color_style().ERROR(
            "NOTE: You will need to run the following command to create the needed Karma config templates before "
            "running this command.\n"
            "  python manage.py makeangularsite"
        )

        # Check and see if templates exist
        template_path = os.path.join(self.get_default_site_app(), self.template_dir)
        if os.path.exists(template_path) and os.path.isdir(template_path):
            filename_matches = [re.match(r'^karma-(.*).conf.js$', filename)
                                for filename in os.listdir(template_path)]
            template_types = [match.group(1) for match in filename_matches if match]

            if len(template_types):
                types_message = '\n'.join(["The following types of Karma tests are available:"] +
                                          ["  %s%s" % (test_type, '*' if test_type == self.default_test_type else '')
                                           for test_type in template_types] +
                                          ["", "If no apps are listed, tests from all the INSTALLED_APPS will be run."])

        # Append template message to standard usage
        parent_usage = super(Command, self).usage(subcommand)
        return "%s\n\n%s" % (parent_usage, types_message)

    def handle(self, test_type=None, *args, **options):
        self.verbosity = int(options.get('verbosity'))
        self.test_type = test_type or self.default_test_type

        # Determine template location
        karma_config_template = \
            os.path.join(self.get_default_site_app(), self.template_dir, 'karma-%s.conf.js' % self.test_type)
        if self.verbosity >= 2:
            self.stdout.write("Using karma template: %s" % karma_config_template)

        if not os.path.exists(karma_config_template):
            raise IOError("Karma template %s was not found." % karma_config_template)

        # Establish the Context for the template
        if options.get('greedy', False):
            app_paths = ['**']
            if self.verbosity >= 2:
                self.stdout.write("Running %s tests for all applications in the project." % self.test_type)
        elif len(args):
            app_paths = self.get_existing_apps_from(set(args) & set(settings.INSTALLED_APPS))
        else:
            app_paths = self.get_existing_apps_from(settings.INSTALLED_APPS)

        context = template.Context(dict(options, **{
            'app_paths': app_paths,
            'djangular_root': self.get_djangular_root()
        }), autoescape=False)

        # Establish the template content in memory
        with open(karma_config_template, 'rb') as config_template:
            template_content = config_template.read()
            template_content = template_content.decode('utf-8')
            js_template = template.Template(template_content)
            template_content = js_template.render(context)
            template_content = template_content.encode('utf-8')

            if self.verbosity >= 3:
                self.stdout.write("\n")
                self.stdout.write("Karma config contents")
                self.stdout.write("---------------------")
                self.stdout.write(template_content)
                self.stdout.write("\n")

        if not template_content:
            raise IOError("The produced Karma config was empty.")

        # Write the template content to the temp file and close it, so the karma process can read it
        temp_config_file = tempfile.NamedTemporaryFile(suffix='.conf.js', prefix='tmp_karma_',
                                                       dir=self.get_default_site_app(),
                                                       delete=False)  # Manually delete so subprocess can read
        try:
            temp_config_file.write(template_content)
            temp_config_file.close()

            # Start the karma process
            self.stdout.write("\n")
            self.stdout.write("Starting Karma Server (https://github.com/karma-runner/karma)\n")
            self.stdout.write("-------------------------------------------------------------\n")

            subprocess.call(['karma', 'start', temp_config_file.name])

        # When the user kills the karma process, do nothing, then remove the temp file
        except KeyboardInterrupt:
            pass
        finally:
            os.remove(temp_config_file.name)
