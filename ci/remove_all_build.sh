#!/usr/bin/env bash

docker-compose down && docker volume remove tyme_bank_postgres_data
docker rmi tyme_bank_frontend tyme_bank_web
