import io
import pandas as pd
from django.apps import apps
from django.core.management.base import BaseCommand
from databricks.sdk import WorkspaceClient

from config import settings

class Command(BaseCommand):
    help = 'Export core.models.MyModel queryset to Parquet and upload to Databricks DBFS'

    def add_arguments(self, parser):
        parser.add_argument('--model', type=str, help='Django model to export in the format app_label.ModelName')

    def handle(self, *args, **options):
        model = options['model']

        # Validate provided model
        try:
            app_label, model_name = model.split('.')
            model = apps.get_model(app_label, model_name)
        except (ValueError, LookupError):
            self.stdout.write(self.style.ERROR('Invalid model name'))
            return

        # Convert queryset to DataFrame
        queryset = model.objects.all().values()
        df = pd.DataFrame(list(queryset))

        # Write DataFrame to a buffer in Parquet format
        buffer = io.BytesIO()
        df.to_csv(buffer)
        buffer.seek(0)

        # Initialize Databricks Workspace client
        w = WorkspaceClient(
            host=settings.DATABRICKS_INSTANCE,
            token=settings.DATABRICKS_TOKEN
        )

        # Full destination path in DBFS
        full_dbfs_path = f"{settings.DBFS_PATH}/main.csv"

        try:
            # Upload file to DBFS using Databricks SDK
            w.dbfs.upload(path=full_dbfs_path, src=buffer, overwrite=True)
            self.stdout.write(self.style.SUCCESS(f'Uploaded csv to Databricks DBFS: {full_dbfs_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to upload file to Databricks DBFS: {e}"))
