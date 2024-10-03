#!/usr/bin/env bash

docker-compose up -d
read -p "Pausing for 5 seconds" -t 5
docker exec -it tyme_bank_web_1 bash ../ci/migrations.sh
