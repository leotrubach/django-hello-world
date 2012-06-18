from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_models
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Displays count of models in database'

    def handle(self, *args, **kwargs):
        for model in get_models():
            model_type = ContentType.objects.get_for_model(model)
            name = '%s.%s' % (model_type.app_label, model_type.model)
            count = model.objects.count()
            output_str = '%s:%s\n' % (name, count)
            self.stdout.write(output_str)
            self.stderr.write('error: ' + output_str)
