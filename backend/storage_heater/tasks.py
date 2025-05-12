import logging

from celery import signals, shared_task
from rest_framework.exceptions import ValidationError

from storage_heater.helpers.mqtt_client import mqtt_service
from storage_heater.serializers import StorageHeaterSerializer

logger = logging.getLogger(__name__)

@signals.worker_ready.connect
def run_mqtt_client(**kwargs):
    """Long-running task that keeps MQTT client connected."""
    try:
        mqtt_service.start()

    except Exception as e:
        return False

@shared_task
def process_mqtt_payload(payload):
    try:
        serializer = StorageHeaterSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Heater status: {payload} has been saved to database")
        return True
    except ValidationError as error:
        logger.error(f'Failed validating data, with error message: {error},')
    except AssertionError as error:
        logger.error(f'Failed saving to db, with error message: {error},')
    return False
