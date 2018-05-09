import gitlab
import iso8601
from celery import shared_task
from django.conf import settings

from dashboard.models import ServiceDeploy


@shared_task
def fetch_gitlab_deployment(user_id):
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
            ServiceDeploy.objects.update_or_create(name=project.name, environment=pipeline.ref, user_id=user_id,
                                                   defaults={
                                                       'deploy_timestamp': iso8601.parse_date(pipeline.finished_at)
                                                   })
