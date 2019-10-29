#!/usr/bin/env bash

openapi-generator generate -g typescript-axios -i swagger.yaml --skip-validate-spec -o moca-client/src/services/openapi/
