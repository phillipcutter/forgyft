[![Build Status](https://travis-ci.com/mrfleap/forgyft.svg?token=ifX93RzwrrnrFqsE8L87&branch=master)](https://travis-ci.com/mrfleap/forgyft)<br />
Development: [![Development Build Status](https://travis-ci.com/mrfleap/forgyft.svg?token=ifX93RzwrrnrFqsE8L87&branch=development)](https://travis-ci.com/mrfleap/forgyft)

Forgyft was an online gift recommendation service developed by Phillip Cutter, Sohum Sanu, Rohan Ganesh, Dhriti Roy, and Aditya Rao for the 2018-2019 TYE Seattle competition.

This project was featured on Seattle's King 5 News in a [TV interview](https://www.youtube.com/watch?v=yMKliSJwpzw).

## Celery

Ensure you are running an AMQP backend server locally, RabbitMQ is a great choice. Then make sure the url to conncet to it
is in `CELERY_BROKER_URL` in `forgyft/settings.py` under the `if DEBUG:` section.'

You can start a worker with this command:

```
celery -A forgyft worker -l info
```

## Docker

Deploy:

docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
