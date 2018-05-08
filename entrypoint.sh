#!/bin/bash
# File: entrypoint.sh
# Description: Inspectorio microservices startup script

set -euxo pipefail

main() {
    config
    exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
}

config() {
    # Ignore if sysctl failed because this maybe don't work inside container
    set +e
    sysctl -w net.core.netdev_max_backlog=4096
    sysctl -w net.core.somaxconn=65535
    set -e

    # Replace ${APP_USER} and ${NGINX_WORKER}
    # Must have in entrypoint.sh
    # shellcheck disable=SC2016
    envsubst '${APP_USER} ${NGINX_WORKER}' < /etc/nginx/nginx.conf | sponge /etc/nginx/nginx.conf

    envsubst < /etc/nginx/conf.d/www.conf | sponge /etc/nginx/conf.d/www.conf
    envsubst < /etc/supervisor/conf.d/uwsgi.conf | sponge /etc/supervisor/conf.d/uwsgi.conf
    # uwsgi already support environment in uwsgi.ini
    # envsubst < "${APP_HOME}/uwsgi.ini" | sponge "${APP_HOME}/uwsgi.ini"
}

main "$@"
