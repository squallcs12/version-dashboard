from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework import viewsets

from dashboard.models import ServiceDeploy
from dashboard.serializers import ServiceDeploySerializer


class ServiceDeployViewSet(viewsets.ModelViewSet):
    queryset = ServiceDeploy.objects.all()
    serializer_class = ServiceDeploySerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        try:
            service_deploy = ServiceDeploy.objects.get(name=data['name'], environment=data['environment'])
        except ServiceDeploy.DoesNotExist:
            serializer.save()
        else:
            service_deploy.deploy_timestamp = timezone.now()
            service_deploy.save()


class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'service_deploys': ServiceDeploy.objects.all().order_by('name'),
        })
        return context