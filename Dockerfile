FROM inspectorio/python:3.6
MAINTAINER Inspectorio DevOps <devops@inspectorio.com>

ARG SSH_PRIVATE_KEY

RUN pipenv install --system --deploy && chown -R "${APP_USER}":"${APP_GRP}" "${APP_HOME}"
