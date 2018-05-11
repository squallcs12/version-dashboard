from django.conf import settings
from django.db import models
from django.utils import timezone


class ServiceDeploy(models.Model):
    name = models.CharField(max_length=255)
    environment = models.CharField(max_length=30)
    deploy_timestamp = models.DateTimeField(default=timezone.now, blank=True)
    previous_deploy_timestamp = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    version = models.CharField(max_length=50, default='', blank='')

    class Meta:
        unique_together = (
            ('name', 'environment', 'user'),
        )

    @property
    def is_deployed_today(self):
        return self.deploy_timestamp.date() == timezone.now().date()

    @property
    def is_deployed_yesterday(self):
        return self.deploy_timestamp.date() == timezone.now().date() - timezone.timedelta(days=1)

    def calculate_duration(self, start, end):
        if not start:
            return ''

        diff = end - start
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

    @property
    def previous_duration(self):
        return self.calculate_duration(self.previous_deploy_timestamp, self.deploy_timestamp)

    @property
    def duration(self):
        return self.calculate_duration(self.deploy_timestamp, timezone.now())
