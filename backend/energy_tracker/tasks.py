import logging
from celery import shared_task
from django.conf import settings
from energy_tracker.client import PC321MeterClient
import subprocess
import os
from datetime import datetime
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
        success = client.fetch_and_process_data()

        if success:
            return True

        else:
            logger.error(f"Failed to fetch data for device {device['device_id']}")
            return False
            
    except Exception as e:
        logger.exception(f"Error in fetch_and_save_energy_data task: {e}")
        return False

@shared_task
def backup_database():
    """
    Celery task to backup the PostgreSQL database using pg_dump.
    """
    backup_dir = '/app/backups'
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"backup_{timestamp}.sql"
    filepath = os.path.join(backup_dir, filename)
    
    db_url = settings.DATABASE_URL
    if not db_url:
        logger.error("DATABASE_URL not found. Cannot perform backup.")
        return False
        
    try:
        subprocess.run(
            ['pg_dump', db_url, '-f', filepath],
            check=True,
            capture_output=True
        )
        logger.info(f"Database backup created successfully: {filepath}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Database backup failed: {e.stderr.decode('utf-8')}")
        return False
    except Exception as e:
        logger.exception(f"Error during database backup: {e}")
        return False