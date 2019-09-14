#!/usr/bin/env bash
docker rm -f moca_service
docker rm -f moca_db
docker volume rm moca_moca-db-volume
sleep 5 
docker-compose up 
sleep 5 
