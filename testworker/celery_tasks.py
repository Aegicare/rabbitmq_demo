"""weaver_worker.py
Usage::
    $ celery -A weaver_worker worker --app=celery_tasks:app  -l info
"""
from __future__ import absolute_import, unicode_literals
from celery import Celery, current_task


def create_app(config):
    """Create a celery app instance."""
    celery_app = Celery("weaver_worker")
    celery_app.config_from_object(config)
    return celery_app


app = create_app('settings')


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


def fib_recursion(n):
    """ 故意让时间很长很长"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_recursion(n - 1) + fib_recursion(n - 2)


@app.task(name='weaver_analysis', bind=True, default_retry_delay=3, max_retries=1)
def weaver_analysis(self, n):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
        self.request))
    try:
        result_list = []
        for i in range(n):
            result = fib_recursion(i)
            result_list.append(result)
            process_percent = int(100 * float(i) / float(n))
            current_task.update_state(state='PROGRESS', meta={'process_percent': process_percent})
    except Exception as exc:
        # overrides the default delay to retry after xxx
        raise self.retry(exc=exc, countdown=2)
    return result_list
