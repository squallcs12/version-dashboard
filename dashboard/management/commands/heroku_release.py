from django.core.management import BaseCommand

from dashboard.tasks import fetch_gitlab_deployment


class Command(BaseCommand):
    def handle(self, *args, **options):
        fetch_gitlab_deployment.delay(2)
