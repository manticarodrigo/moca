#!/usr/bin/env bash

if [ -z ${service+x} ]; then
  export service="http://localhost:8000"
fi

if [ -z ${service_container+x} ]; then
  export service_container="moca_service"
fi

function dexec () {
  docker exec -i ${service_container} $@
}

function dbexec () {
  echo $@ | dexec python apps/manage.py dbshell
}

# dbexec truncate moca_user cascade
dexec rm -rf htmlcov
dexec coverage run apps/manage.py test moca.tests -v 2 &&
dexec coverage html &&
dexec coverage report &&
./integration/update_swagger.sh &&
./integration/generate_ts.sh
