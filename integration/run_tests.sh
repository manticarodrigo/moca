#!/usr/bin/env bash

if [ -z ${service+x} ]; then
  export service="http://localhost:8000"
fi

if [ -z ${service_container+x} ]; then
  export service_container="moca_service"
fi

if [ -z ${run_cleanup+x} ]; then
  export runCleanup="1"
fi

if [ -n runCleanup ]; then
  echo "truncate moca_user cascade" | docker exec -i ${service_container} python apps/manage.py dbshell
fi

(cd integration/tests; PYTHONPATH=$(pwd) py.test $@)
