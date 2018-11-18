#!/usr/bin/env bash

has_nocollect_option=false
while getopts :hn opn; do
    case $opn in
        n) has_nocollect_option=true ;;
        :) echo "Missing argument for option -$OPTARG"; exit 1;;
       \?) echo "Unknown option -$OPTARG"; exit 1;;
    esac
done

# here's the key part: remove the parsed options from the positional params
shift $(( OPTIND - 1 ))

if $has_nocollect_option; then
	echo "Not collecting staticfiles"
else
	echo "Collecting static"
	export COLLECT_STATIC=1
fi

eval $(docker-machine env forgift)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --compress
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f