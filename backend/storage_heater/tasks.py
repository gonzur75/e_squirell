
from celery import signals
from storage_heater.helpers.mqtt_client import mqtt_service


@signals.worker_ready.connect
def run_mqtt_client(**kwargs):
    """Long-running task that keeps MQTT client connected."""
    try:
        mqtt_service.start()

    except Exception as e:
        return False
