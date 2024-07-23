# myapp/management/commands/celery.py

from django.core.management.base import BaseCommand, CommandError
import subprocess


class Command(BaseCommand):
    help = 'Manage Celery worker and Flower'

    def add_arguments(self, parser):
        parser.add_argument('service', type=str, help='Specify the service to run: worker or flower')
        parser.add_argument('--port', type=int, default=5555, help='Port to run Flower on')

    def handle(self, *args, **options):
        service = options['service']
        port = options['port']

        if service == 'worker':
            self.stdout.write(self.style.SUCCESS('Starting Celery worker...'))
            subprocess.call(['celery', '-A', 'django_otp', 'worker', '--loglevel=info'])
        elif service == 'flower':
            self.stdout.write(self.style.SUCCESS(f'Starting Flower on port {port}...'))
            subprocess.call(['celery', '-A', 'django_otp', 'flower', f'--port == {str(port)}'])
        else:
            raise CommandError('Invalid service specified. Use "worker" or "flower".')