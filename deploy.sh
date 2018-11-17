#!/usr/bin/env bash

eval $(docker-machine env forgift)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --compress
export COLLECT_STATIC=1
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f