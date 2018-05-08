FROM inspectorio/python:3.6
MAINTAINER Inspectorio DevOps <devops@inspectorio.com>


RUN pipenv install --system --deploy\
 && chown -R "${APP_USER}":"${APP_GRP}" "${APP_HOME}"
