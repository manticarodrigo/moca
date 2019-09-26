#!/usr/bin/env bash

if [ -z ${service+x} ]; then
  export service="http://localhost:8000"
  runCleanup="1"
fi

if [ -n runCleanup ]; then
  echo "truncate moca_user cascade" | docker exec -i moca_service python apps/manage.py dbshell
fi

(cd integration/tests; PYTHONPATH=$(pwd) py.test $@)
