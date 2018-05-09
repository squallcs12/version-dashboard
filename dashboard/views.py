from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework import viewsets, permissions

from dashboard.models import ServiceDeploy
from dashboard.serializers import ServiceDeploySerializer


class ServiceDeployViewSet(viewsets.ModelViewSet):
    queryset = ServiceDeploy.objects.all()
    serializer_class = ServiceDeploySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super(ServiceDeployViewSet, self).get_queryset()
        queryset = queryset.filter(user=self.queryset.user)
        return queryset

    def perform_create(self, serializer):
        data = serializer.validated_data
        try:
            service_deploy = ServiceDeploy.objects.get(name=data['name'], environment=data['environment'],
                                                       user=self.request.user)
        except ServiceDeploy.DoesNotExist:
            serializer.save(user=self.request.user)
        else:
            service_deploy.deploy_timestamp = timezone.now()
            service_deploy.save()


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        service_deploys = ServiceDeploy.objects.filter(user=self.request.user).order_by('name')
        environments = sorted(set(service_deploys.values_list('environment', flat=True)))

        context.update({
            'service_deploys': service_deploys,
            'environments': environments,
        })
        return context
