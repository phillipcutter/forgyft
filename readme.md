[![Build Status](https://travis-ci.com/mrfleap/forgyft.svg?token=ifX93RzwrrnrFqsE8L87&branch=master)](https://travis-ci.com/mrfleap/forgyft)<br />
Development: [![Development Build Status](https://travis-ci.com/mrfleap/forgyft.svg?token=ifX93RzwrrnrFqsE8L87&branch=development)](https://travis-ci.com/mrfleap/forgyft)<br />
Welcome to the Forgift source code!

## Celery

Ensure you are running an AMQP backend server locally, RabbitMQ is a great choice. Then make sure the url to conncet to it
is in `CELERY_BROKER_URL` in `forgyft/settings.py` under the `if DEBUG:` section.'

You can start a worker with this command:
~~~
celery -A forgyft worker -l info
~~~