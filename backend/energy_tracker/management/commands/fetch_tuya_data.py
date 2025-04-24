
import time
import logging
from django.core.management.base import BaseCommand

from config import settings
from energy_tracker.client import PC321MeterClient


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch data from Tuya smart meter using tinytuya and save to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=300,
            help='Interval in seconds between fetches'
        )
        parser.add_argument(
            '--continuous',
            action='store_true',
            help='Run continuously with specified interval'
        )
        parser.add_argument(
            '--device-id',
            type=str,
            help='Override device ID from settings'
        )
        parser.add_argument(
            '--device-ip',
            type=str,
            help='Override device IP from settings'
        )
        parser.add_argument(
            '--local-key',
            type=str,
            help='Override local key from settings'
        )

    def handle(self, *args, **options):
        try:
            device = settings.SMART_METER
            if options['device_id'] and options['device_ip'] and options['local_key']:
                device = {
                    'device_id': options['device_id'],
                    'device_ip': options['device_ip'],
                    'local_key': options['local_key'],
                    'device_version': 3.4  # Default version
                }

        except AttributeError as e:
            self.stderr.write(f"Missing configuration: {e}")
            return

        interval = options['interval']
        continuous = options['continuous']

        self.stdout.write(f"Starting Tuya data collection {'continuously' if continuous else 'once'}")

        try:
            while True:
                client = PC321MeterClient(
                    device_id=device['device_id'],
                    device_ip=device['device_ip'],
                    local_key=device['local_key'],
                    device_version=device.get('device_version', 3.4)
                )

                success = client.fetch_and_save()
                if success:
                    self.stdout.write(f"Successfully fetched data for device {device['device_id']}")
                else:
                    self.stderr.write(f"Failed to fetch data for device {device['device_id']}")

                if not continuous:
                    break

                self.stdout.write(f"Sleeping for {interval} seconds")
                time.sleep(interval)

        except KeyboardInterrupt:
            self.stdout.write("Data collection stopped by user")

        except Exception as e:
            self.stderr.write(f"Error: {e}")
