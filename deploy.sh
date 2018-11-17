#!/usr/bin/env bash

eval $(docker-machine env forgift)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml run -e COLLECT_STATIC=1 web -d
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f