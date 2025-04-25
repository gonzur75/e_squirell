# e_squirell

## Celery Integration for Asynchronous Tasks

This document describes the integration of Celery for asynchronous task processing in the e_squirell project.

### Overview

The project uses Celery with Redis as a message broker to handle asynchronous tasks, particularly for data processing. This allows the application to offload time-consuming operations to background workers, improving responsiveness and scalability.

### Components

1. **Celery**: A distributed task queue system
2. **Redis**: Used as the message broker and result backend
3. **Celery Beat**: For scheduling periodic tasks
4. **Flower**: A web-based tool for monitoring and administrating Celery clusters

### Available Tasks

#### Energy Tracker App

##### `fetch_and_save_energy_data`

This task fetches data from the Tuya smart meter and saves it to the database. It can be scheduled to run periodically using Celery Beat.

### Usage

#### Running a Task Manually

You can run tasks manually using the provided management commands or through the Django shell.

#### Scheduling Tasks

Tasks can be scheduled in two ways:

1. **Using settings.py**: Tasks can be scheduled by default through the `CELERY_BEAT_SCHEDULE` configuration in settings.py.

   Example: The `fetch_and_save_energy_data` task is scheduled to run every minute by default.

2. **Using Django Admin**: Tasks can be scheduled through the Django Admin interface after logging in:

   1. Go to Django Admin
   2. Navigate to "Periodic Tasks" under the "DJANGO CELERY BEAT" section
   3. Click "ADD PERIODIC TASK"
   4. Select the task (e.g., "energy_tracker.tasks.fetch_and_save_energy_data")
   5. Set the schedule (interval, crontab, etc.)
   6. Save the task

Note: Tasks scheduled through the Django Admin interface will override the default schedule defined in settings.py.

### Monitoring Tasks with Flower

Flower is a web-based tool for monitoring and administrating Celery clusters. It provides real-time monitoring of task execution, worker status, and resource usage.

#### Accessing Flower

Once the services are running, you can access the Flower dashboard at:

```
http://localhost:5555
```

#### Features

- Real-time monitoring of task execution
- View task details, arguments, and results
- Monitor worker status and resource usage
- Cancel or terminate running tasks
- View statistics and graphs of task execution

### Docker Setup

The Docker Compose configuration includes:

1. **Redis**: Message broker and result backend
2. **Celery Worker**: Processes the tasks
3. **Celery Beat**: Schedules periodic tasks
4. **Flower**: Provides a web dashboard for monitoring tasks

To start all services:

```bash
docker-compose up -d
```

### Development

To add new tasks:

1. Define the task in your app's `tasks.py` file using the `@shared_task` decorator
2. Implement the task logic
3. Schedule the task using Celery Beat if needed

Example:

```python
from celery import shared_task

@shared_task
def my_new_task():
    # Task implementation
    pass
```
