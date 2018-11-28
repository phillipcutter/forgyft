#!/usr/bin/env bash

COLLECT_STATIC=0
docker-compose down
docker-compose build --compress
docker-compose up -d
docker-compose ps

attempt_counter=0
max_attempts=15

until $(curl --output /dev/null --silent --head --fail http://localhost); do
    if [ ${attempt_counter} -eq ${max_attempts} ];then
      echo "Max attempts reached"
      exit 1
    fi

    printf '.'
    attempt_counter=$(($attempt_counter+1))
    sleep 1
done


web_response=`curl -sL \
    -w "%{http_code}\\n" \
    "http://localhost" \
    -o /dev/null \
    --connect-timeout 10 \
    --max-time 30`

echo $web_response

if [[ $web_response == "200" ]] ;
then
   echo "Server OK" ;
else
   echo "Server not OK, responded with $web_response" ;
   exit 1
fi
exit 0