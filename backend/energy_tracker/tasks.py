import logging
from celery import shared_task
from django.conf import settings
from energy_tracker.client import PC321MeterClient

logger = logging.getLogger(__name__)

@shared_task
def fetch_and_save_energy_data():
    """
    Celery task to fetch data from Tuya smart meter and save to database.
    This task can be scheduled to run periodically using Celery Beat.
    """
    try:
        device = settings.SMART_METER
        
        client = PC321MeterClient(**device)
        
        success = client.fetch_and_save()
        if success:
            return True
        else:
            logger.error(f"Failed to fetch data for device {device['device_id']}")
            return False
            
    except Exception as e:
        logger.exception(f"Error in fetch_and_save_energy_data task: {e}")
        return False