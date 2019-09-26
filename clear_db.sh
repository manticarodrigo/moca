#!/usr/bin/env bash
echo "truncate moca_user cascade" | docker exec -i moca_service python apps/manage.py dbshell

