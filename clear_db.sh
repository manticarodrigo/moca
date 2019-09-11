#!/usr/bin/env bash

docker rm -f moca_db
docker volume rm moca_moca-db-volume
docker-compose up -d db

sleep 8

docker exec -it moca_service python apps/manage.py makemigrations moca
docker exec -it moca_service python apps/manage.py migrate
