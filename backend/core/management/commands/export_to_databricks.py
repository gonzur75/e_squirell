import io
from datetime import timedelta

import pandas as pd
from databricks.sdk import WorkspaceClient
from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils import timezone

from config import settings


class Command(BaseCommand):
    """
    Exports a Django model queryset to a CSV file and uploads it to Databricks DBFS.

    Usage:
        python manage.py export_to_databricks --model app_label.ModelName
        python manage.py export_to_databricks --model app_label.ModelName --last_day

    Arguments:
        --model Django model to export in the format app_label.ModelName
        --last_day (optional) Limit export to objects from the last 24 hours

    Example:
        python manage.py export_to_databricks --model core.MyModel
        python manage.py export_to_databricks --model core.MyModel --last_day
    """
    help = 'Export core.models.MyModel queryset to Parquet and upload to Databricks DBFS'

    def add_arguments(self, parser):
        parser.add_argument('--model', type=str, help='Django model to export in the format app_label.ModelName')
        parser.add_argument('--last_day', action='store_true', help='Limit export to objects from the last 24 hours')

    def handle(self, *args, **options):
        model = options['model']

        now = timezone.now()
        last_24h = now - timedelta(hours=24)

        try:
            app_label, model_name = model.split('.')
            model = apps.get_model(app_label, model_name)
        except (ValueError, LookupError):
            self.stdout.write(self.style.ERROR('Invalid model name'))
            return

        if options['last_day']:
            queryset = model.objects.filter(timestamp__gte=last_24h).values()
            full_dbfs_path = f"{settings.DBFS_PATH}/{model_name}_{now:%Y%m%d_%H%M%S}.csv"
        else:
            queryset = model.objects.all().values()
            full_dbfs_path = f"{settings.DBFS_PATH}/{model_name}_main.csv"

        df = pd.DataFrame(list(queryset))

        buffer = io.BytesIO()
        df.to_csv(buffer)
        buffer.seek(0)


        w = WorkspaceClient(
            host=settings.DATABRICKS_INSTANCE,
            token=settings.DATABRICKS_TOKEN
        )

        try:
            w.dbfs.upload(path=full_dbfs_path, src=buffer, overwrite=True)
            self.stdout.write(self.style.SUCCESS(f'Uploaded csv to Databricks DBFS: {full_dbfs_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to upload file to Databricks DBFS: {e}"))
