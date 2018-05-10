import gitlab
import iso8601
from celery import shared_task
from django.conf import settings

from dashboard.models import ServiceDeploy


@shared_task(autoretry_for=(Exception,))
def fetch_gitlab_deployment(user_id):
    environments = ['prod', 'preprod', 'staging']

    gl = gitlab.Gitlab('https://gitlab.inspectorio.com/', private_token=settings.GITLAB_PRIVATE_TOKEN,
                       api_version='4')
    projects = gl.projects.list(per_page=1000)
    for project in projects:
        if not project.path_with_namespace.startswith('saas/'):
            continue

        for environment in environments:

            pipelines = project.pipelines.list(status='success', per_page=2, ref=environment)
            if not pipelines:
                continue

            pipeline = pipelines[0]
            pipeline = project.pipelines.get(pipeline.id)
            timestamp = iso8601.parse_date(pipeline.finished_at)

            try:
                service = ServiceDeploy.objects.get(name=project.name, environment=environment, user_id=user_id)
                if service.deploy_timestamp == timestamp:
                    continue

                service.previous_deploy_timestamp = service.deploy_timestamp
                service.deploy_timestamp = timestamp
                service.save()
            except ServiceDeploy.DoesNotExist:

                previous_deploy_timestamp = None
                if len(pipelines) > 1:
                    pipeline = pipelines[1]
                    pipeline = project.pipelines.get(pipeline.id)
                    previous_deploy_timestamp = iso8601.parse_date(pipeline.finished_at)

                ServiceDeploy.objects.create(name=project.name, environment=pipeline.ref, user_id=user_id,
                                             deploy_timestamp=timestamp,
                                             previous_deploy_timestamp=previous_deploy_timestamp)

    fetch_gitlab_deployment.apply_async(args=[user_id], countdown=5)
