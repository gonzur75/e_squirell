from celery import shared_task
from django.core.management import call_command

@shared_task
def export_to_databricks_task():
    call_command(
        'export_to_databricks',
        '--model', 'energy_tracker.EnergyLog',
        '--last_day'
    )
    call_command(
        'export_to_databricks',
        '--model', 'storage_heater.StorageHeater',
        '--last_day'
    )
    return True