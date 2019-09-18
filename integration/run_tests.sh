#!/usr/bin/env bash

if [ -z ${service+x} ]; then
  export service="http://localhost:8000"
fi

(cd integration/tests; PYTHONPATH=$(pwd) py.test)
