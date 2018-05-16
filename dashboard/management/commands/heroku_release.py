from django.core.management import BaseCommand, call_command

from dashboard.tasks import fetch_gitlab_deployment


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('migrate')
        fetch_gitlab_deployment.delay(2)
