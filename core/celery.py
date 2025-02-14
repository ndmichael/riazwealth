from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed Django apps
app.autodiscover_tasks()

# Define the Celery Beat Schedule
app.conf.beat_schedule = {
    'accrue_daily_profits': {
        'task': 'users.tasks.accrue_profits',
        'schedule': crontab(hour=0, minute=0),  # Runs daily at midnight
    },
}

