from celery import shared_task
import requests

from authorize.apps import logger
from django_otp.celery import BaseTaskWithRetry
from django_otp.settings import dolphin_url


@shared_task(bind=True, base=BaseTaskWithRetry)
def sync_member_task(self, details: dict):
    response = requests.post(f'{dolphin_url}/tokens/member', json=details)
    if response.status_code != 200:
        logger.error(response.status_code)
        raise Exception



