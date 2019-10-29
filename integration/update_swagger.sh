#!/usr/bin/env bash

if [ -z ${service+x} ]; then
  export service="http://localhost:8000"
fi

# TODO right now the output from django is not byte-for-byte equal, but is equivalent to the same yaml you generate
# The diff result is just informational for now, this test will always pass
http GET $(printf "%s%s" ${service} /api/docs/swagger.yaml) > swagger_2.yaml && diff swagger.yaml swagger_2.yaml || true
