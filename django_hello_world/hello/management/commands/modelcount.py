from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_models

class Command(BaseCommand):
    help = 'Displays count of models in database'

    def handle(self, *args, **kwargs):
        for model in get_models():
            name = '%s.%s' % (model._meta.app_label, model.__name__)
            count = model.objects.count()
            output_str = '%s:%s\n' % (name, count)
            self.stdout.write(output_str)
            self.stderr.write('error: ' + output_str)