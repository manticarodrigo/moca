#!/usr/bin/env bash

if [ -z ${service+x} ]; then
  export service="http://localhost:8000"
fi

http GET "${service}/api/docs/swagger.yaml" > swagger.yaml && git diff swagger.yaml
