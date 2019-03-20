from kombu import Exchange, Queue

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'  # Default: "json" (since 4.0, earlier: pickle).
CELERY_RESULT_SERIALIZER = 'json'  # Default: json since 4.0 (earlier: pickle).

# sudo rabbitmqctl add_vhost aegis_vhost
# sudo rabbitmqctl add_user aegis aegicare123
# sudo rabbitmqctl set_permissions -p aegis_vhost aegis ".*" ".*" ".*"
# sudo rabbitmqctl set_user_tags aegis management
# RABBIT_HOSTNAME = 'localhost'
# 生产环境密码要配置为环境变量
RABBIT_HOSTNAME = '192.168.56.50'
BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}'.format(
    user='aegis',
    password='aegicare123',
    hostname=RABBIT_HOSTNAME,
    vhost='aegis_vhost'
)

BROKER_HEARTBEAT = '?heartbeat=30'
if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT

# configure queues
CELERY_QUEUES = {
    'celery': {'routing_key': 'celery', },
    'default': {'exchange': 'default', 'routing_key': 'default', },
    'aegis_queue': {'exchange': 'default', 'routing_key': 'default', },
}
# Example:
# CELERY_QUEUES = (
#     Queue('celery', Exchange('celery'), routing_key='celery'),
#     Queue('default', Exchange('default'), routing_key='default'),
#     Queue('post_notcie', Exchange('post_notcie'), routing_key='post.notcie.follower'),
#     Queue('comment_notcie', Exchange('comment_notcie'), routing_key='post.comment.notcie.owner'),
#     Queue('es_update', Exchange('es_update'), routing_key='es.index.update'),
#     Queue('es_delete', Exchange('es_delete'), routing_key='es.index.delete'),
# )
CELERY_DEFAULT_QUEUE = 'celery'
CELERY_TASK_DEFAULT_EXCHANGE = CELERY_DEFAULT_QUEUE
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = CELERY_DEFAULT_QUEUE
CELERY_TASK_DEFAULT_ROUTING_KEY = CELERY_DEFAULT_QUEUE
CELERY_TASK_DEFAULT_DELIVERY_MODE = 'persistent'  # Can be transient (messages not written to disk) or persistent (written to disk).

CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

CELERY_TASK_RESULT_EXPIRES = None  # Default: Expire after 1 day.

# result backbend
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_RESULT_PERSISTENT = True
# use redis to save result of json format
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/4'

CELERYD_PREFETCH_MULTIPLIER = 1
# CELERYD_MAX_TASKS_PER_CHILD = 1000  # Maximum number of tasks a pool worker process can execute before it’s replaced with a new one. Default is no limit.

# monitor
# pip install flower
# celery -A proj flower --port=5555
# celery flower --broker=amqp://aegis:aegicare123@192.168.56.50:5672/aegis_vhost --port=5555

# run in background
# http://docs.celeryproject.org/en/master/getting-started/next-steps.html#in-the-background

