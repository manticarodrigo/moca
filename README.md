# Local setup
This should take care of building and starting everything
```shell
docker-compose up
```

To recreate the docker images used from scratch:
```shell
docker-compose rm
docker-compose build --no-cache
```

# Migrations
In order to create migration scripts
```shell
docker exec -it moca_service makemigrations moca
```

To run migrations:
```shell
docker exec -it moca_service migrate
```
