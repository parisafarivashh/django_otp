from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_otp.settings')

app = Celery('django_otp')
# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.task_queues = {
    'default': {
        'exchange': 'default',
        'exchange_type': 'direct',
        'binding_key': 'default',
    },
    'sync_member': {
        'exchange': 'sync_member',
        'exchange_type': 'direct',
        'binding_key': 'sync_member',
    },
}

app.conf.task_routes = {
    'authorize.tasks.sync_member_task': {'queue': 'sync_member'},
    '*': {'queue': 'default'},
}
