from __future__ import absolute_import
from celery import Celery

# A Celery application named downloaderApp
# A broker on the localhost that will accept message via *Advanced Message Queuing Protocol (AMQP),
#     the protocol used by RabbitMQ
# A response backend where workers will store the return value of the task so that clients can retrieve it later
#     (remember that task execution is asynchronous). If you omit backend, the task will still run, but the return value
#     will be lost. rpc means the response will be sent to a RabbitMQ queue in a Remote Procedure Call pattern.
# Create the app and set the broker location (RabbitMQ)
# cd ../; celery -A test_celery worker --app=test_celery.celery_app:app -l info -P=solo;
app = Celery('test_celery',
             backend='rpc://',
             broker='amqp://aegis:aegicare123@192.168.56.50:5672/aegis_vhost',
             include=['test_celery.tasks'])


# 'amqp://aegis:aegicare123@localhost:5672/myvhost'
# pyamqp://guest@localhost//

