import gitlab
import iso8601
import requests
from collections import defaultdict

from django.conf import settings
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

        environments = ['prod', 'preprod', 'staging']
        service_deploys = []

        gl = gitlab.Gitlab('https://gitlab.inspectorio.com/', private_token=settings.GITLAB_PRIVATE_TOKEN,
                           api_version='4')
        projects = gl.projects.list(per_page=1000)
        for project in projects:
            if not project.path_with_namespace.startswith('saas/'):
                continue
            found = []
            for pipeline in project.pipelines.list(status='success', per_page=100):
                if pipeline.ref not in environments:
                    continue

                if pipeline.ref in found:
                    continue

                pipeline = project.pipelines.get(pipeline.id)

                service_deploys.append({
                    'environment': pipeline.ref,
                    'name': project.name,
                    'deploy_timestamp': iso8601.parse_date(pipeline.finished_at)
                })
                found.append(pipeline.ref)

        context.update({
            'service_deploys': service_deploys,
            'environments': environments,
        })
        return context
