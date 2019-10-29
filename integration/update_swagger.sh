#!/usr/bin/env bash

if [ -z ${service+x} ]; then
  export service="http://localhost:8000"
fi

http GET $(printf "%s%s" ${service} /api/docs/swagger.yaml) > swagger_2.yaml && diff swagger.yaml swagger_2.yaml
