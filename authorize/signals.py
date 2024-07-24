from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from authorize.models import User
from authorize.serializers import RegisterUserResponseSerializer
from authorize.tasks import sync_member_task


@receiver(post_save, sender=User)
def send_user_data(sender, instance, created, **kwargs):
    if created:
        data = RegisterUserResponseSerializer(instance).data
        sync_member_task.apply_async((data,))


@receiver(post_save, sender=User)
def create_admin_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_admin:
            Token.objects.create(user=instance)
