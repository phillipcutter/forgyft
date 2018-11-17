#!/usr/bin/env bash

eval $(docker-machine env forgift)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -e COLLECT_STATIC=1 -d
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f