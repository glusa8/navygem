from django.core.management.base import BaseCommand
from IPython.terminal.ipapp import TerminalIPythonApp

from django.apps import apps
from traitlets.config import Config

class Command(BaseCommand):
    help = 'IPython shell'

    def handle(self, *args, **options):
        import_statements = []

        models = apps.get_models()

        module_to_model_names = {}

        for model in models:
            module_to_model_names.setdefault(model.__module__, [])
            module_to_model_names[model.__module__].append(model.__name__)

        for module, model_names in sorted(module_to_model_names.items()):
            import_statements.append(
                'from {} import {}'.format(module, ', '.join(model_names))
            )

        c = Config()
        c.InteractiveShell.colors = 'lightbg'
        c.TerminalInteractiveShell.highlighting_style = 'legacy'
        c.InteractiveShellApp.exec_lines = ['; '.join(import_statements)]
        c.InteractiveShellApp.exec_lines.append('print "\033[32m{}\033[0m"'.format(
            ', '.join([
                model_name
                for _, model_names in
                sorted(module_to_model_names.items())
                for model_name in
                model_names
            ])
        ))
        plurality = '' if len(models) <= 1 else 's'
        c.InteractiveShellApp.exec_lines.append('print "{} model{} loaded"'.format(len(models), plurality))
        app = TerminalIPythonApp.instance(config=c)
        app.initialize(argv=[])
        app.start()
