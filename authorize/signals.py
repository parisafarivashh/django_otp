from django.db.models.signals import post_save
from django.dispatch import receiver

from authorize.models import User
from authorize.serializers import RegisterUserResponseSerializer
from authorize.tasks import send_data


@receiver(post_save, sender=User)
def send_user_data(sender, instance, created, **kwargs):
    if created:
        data = RegisterUserResponseSerializer(instance).data
        send_data.apply_async((data,))

