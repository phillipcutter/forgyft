#!/usr/bin/env bash

COLLECT_STATIC=0
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --compress
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps
exit 0