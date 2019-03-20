from __future__ import absolute_import
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_try.settings')

from django.conf import settings
from celery import Celery

app = Celery('celery_try')

# 生产环境密码要配置为环境变量
# $ CELERY_CONFIG_MODULE="celeryconfig.prod" celery worker -l info
# app.config_from_envvar('CELERY_CONFIG_MODULE')
app.config_from_object('django.conf:settings')

# For autodiscover_tasks to work, you must define your tasks in a file called 'tasks.py'.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

# run command: celery -A celery_try worker -l info -P solo