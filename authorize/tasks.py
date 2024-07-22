from celery import shared_task


@shared_task(queue='sync_member')
def send_data(details: dict):
    # response = requests.post(f'{url}/member/create', json=data)
    # return response.status_code
    return details

