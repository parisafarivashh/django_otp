import logging

from django.apps import AppConfig


logger = logging.getLogger('django')


class AuthorizeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authorize'

    def ready(self):
        import authorize.signals

