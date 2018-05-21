import gitlab
import iso8601
import re
from celery import shared_task
from django.conf import settings

from dashboard.models import ServiceDeploy


@shared_task(autoretry_for=(Exception,))
def fetch_gitlab_deployment(user_id):
    environments = ['prod', 'preprod', 'staging']
    tag_to_environment = {
        'rc': 'preprod',
    }

    gl = gitlab.Gitlab('https://gitlab.inspectorio.com/', private_token=settings.GITLAB_PRIVATE_TOKEN,
                       api_version='4')
    projects = gl.projects.list(per_page=1000)
    for project in projects:
        if not project.path_with_namespace.startswith('saas/'):
            continue

        pipelines = project.pipelines.list(status='success', per_page=100)
        if not pipelines:
            continue

        found = []
        for pipeline in pipelines:
            environment = pipeline.ref
            if environment not in environments:
                match = re.match(r'^v(\d+)\.(\d+)\.(\d+)(-(.*)\.(\d+))?$', environment)
                match2 = re.match(r'^release-v(\d+)\.(\d+)\.(\d+)?$', environment)
                if match:
                    groups = match.groups()
                    if (len(groups) == 3) or (groups[-1] is None):
                        environment = 'prod'
                    else:
                        environment = tag_to_environment.get(groups[4])
                        if not environment:
                            break
                elif match2:
                    environment = 'staging'
                else:
                    continue

            if environment in found:
                continue
            if set(found) == set(environments):
                break

            found.append(environment)

            pipeline = project.pipelines.get(pipeline.id)
            timestamp = iso8601.parse_date(pipeline.finished_at)

            try:
                service = ServiceDeploy.objects.get(name=project.name, environment=environment, user_id=user_id)
                if service.deploy_timestamp == timestamp:
                    continue

                service.previous_deploy_timestamp = service.deploy_timestamp
                service.deploy_timestamp = timestamp
                service.version = pipeline.ref
                service.save()
            except ServiceDeploy.DoesNotExist:
                previous_deploy_timestamp = None
                ServiceDeploy.objects.create(name=project.name, environment=environment, user_id=user_id,
                                             deploy_timestamp=timestamp, version=pipeline.ref,
                                             previous_deploy_timestamp=previous_deploy_timestamp)

    fetch_gitlab_deployment.apply_async(args=[user_id], countdown=5)
