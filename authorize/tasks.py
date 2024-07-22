from celery import shared_task


@shared_task()
def sync_member_task(details: dict):
    # response = requests.post(f'{url}/member/create', json=data)
    # return response.status_code
    return details

