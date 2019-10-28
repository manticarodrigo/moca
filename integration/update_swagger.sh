#!/usr/bin/env bash

if [ -z ${service+x} ]; then
  export service="http://localhost:8000"
fi

http ${service}/api/docs/swagger.yaml --download
