from django.conf import settings
from django.db import models
from django.utils import timezone


class ServiceDeploy(models.Model):
    name = models.CharField(max_length=255)
    environment = models.CharField(max_length=30)
    deploy_timestamp = models.DateTimeField(default=timezone.now, blank=True)
    previous_deploy_timestamp = models.DateTimeField(default=timezone.now, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    @property
    def is_deployed_today(self):
        return self.deploy_timestamp.date() == timezone.now().date()

    @property
    def duration(self):
        if not self.previous_deploy_timestamp:
            return None
        diff = self.deploy_timestamp - self.previous_deploy_timestamp
        times = []
        if diff.days:
            times.append('{}d'.format(diff.days))
        if diff.seconds:
            hours = int(diff.seconds / 3600)

            secs = diff.seconds % 3600
            mins = int(secs / 60)
            secs = secs % 60

            if hours:
                times.append('{}h'.format(hours))

            if not diff.days:
                times.append('{}m'.format(mins))
                if not hours:
                    times.append('{}s'.format(secs))
        return ' '.join(times)
