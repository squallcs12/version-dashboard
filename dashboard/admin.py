from django.contrib import admin

from dashboard.models import ServiceDeploy


class ServiceDeployAdmin(admin.ModelAdmin):
    list_display = ('name', 'environment', 'deploy_timestamp')
    list_filter = ('environment',)


admin.site.register(ServiceDeploy, ServiceDeployAdmin)
