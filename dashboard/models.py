from django.db import models
from django.utils import timezone


class ServiceDeploy(models.Model):
    name = models.CharField(max_length=255)
    environment = models.CharField(max_length=30)
    deploy_timestamp = models.DateTimeField(default=timezone.now, blank=True)

    @property
    def is_deployed_today(self):
        return self.deploy_timestamp.date() == timezone.now().date()
