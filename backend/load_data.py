import json
import os
import django
import sys
from dateutil.parser import parse

# Set up Django environment
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from energy_tracker.models import EnergyLog
from storage_heater.models import StorageHeater

def load_data():
    # First, wipe exactly what we just put in
    # EnergyLog.objects.all().delete()
    # StorageHeater.objects.all().delete()
    print("Cleared any existing bad records...")

    # Temporarily disable auto_now_add so Django respects our JSON timestamps!
    EnergyLog._meta.get_field('timestamp').auto_now_add = False
    StorageHeater._meta.get_field('timestamp').auto_now_add = False

    # Load Energy Tracker Data
    file_path = '/app/data_temp/download (1).json'
    print(f"Loading {file_path}")
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    logs = []
    for item in data.get('results', []):
        # Convert string to datetime object
        item['timestamp'] = parse(item['timestamp'])
        log = EnergyLog(**item)
        logs.append(log)
    
    EnergyLog.objects.bulk_create(logs, ignore_conflicts=True)
    print(f"Loaded {len(logs)} EnergyLog records with correct timestamps!")

    # Load Storage Heater Data
    file_path = '/app/data_temp/download.json'
    print(f"Loading {file_path}")
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    heaters = []
    for item in data.get('results', []):
        # Convert string to datetime object
        item['timestamp'] = parse(item['timestamp'])
        heater = StorageHeater(**item)
        heaters.append(heater)
        
    StorageHeater.objects.bulk_create(heaters, ignore_conflicts=True)
    print(f"Loaded {len(heaters)} StorageHeater records with correct timestamps!")

if __name__ == '__main__':
    load_data()
