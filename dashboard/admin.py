from django.contrib import admin

from dashboard.models import ServiceDeploy


class ServiceDeployAdmin(admin.ModelAdmin):
    list_display = ('name', 'environment', 'deploy_timestamp', 'version')
    list_filter = ('environment', 'user')
    search_fields = ('name',)


admin.site.register(ServiceDeploy, ServiceDeployAdmin)
