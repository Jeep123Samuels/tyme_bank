#!/usr/bin/env bash

docker-compose up -d
docker exec -it tyme_bank_web_1 bash ../ci/migrations.sh
