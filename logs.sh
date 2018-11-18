#!/usr/bin/env bash

eval $(docker-machine env forgift)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f $1