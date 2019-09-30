#!/usr/bin/env bash

if [ -z ${service+x} ]; then
  export service="http://localhost:8000"
fi

if [ -z ${service_container+x} ]; then
  export service_container="moca_service"
fi

echo "truncate moca_user cascade" | docker exec -i ${service_container} python apps/manage.py dbshell

(cd integration/tests; PYTHONPATH=$(pwd) py.test $@)
