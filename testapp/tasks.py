import time

from celery import shared_task, current_task
from celery.result import AsyncResult
from celery_once import QueueOnce


def fib_recursion(n):
    """ 故意让时间很长很长"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_recursion(n - 1) + fib_recursion(n - 2)


@shared_task
def fib_list(n):
    result_list = []
    for i in range(n):
        result = fib_recursion(i)
        result_list.append(result)
        process_percent = int(100 * float(i) / float(n))
        current_task.update_state(state='PROGRESS', meta={'process_percent': process_percent})
    return result_list


@shared_task
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
        uuid, exc, result.traceback))


@shared_task(name='import_analysis_result', base=QueueOnce, once={'graceful': True, 'keys': ['file_path'], 'timeout': 60 * 60 * 10})
def import_analysis_result(file_path):
    """
    graceful: set to True, instead of raising an AlreadyQueued exception
    keys: creates a lock based on the task's name and its arguments and values
        example key: qo_testapp.tasks.import_analysis_result_file_path-/data/AS8888_v1.txt value:9fcb8bde4bb611e9b6775413797952f7
    timeout: clear a lock after 60 minutes
    :param file_path: v0 file path
    :return:
    """
    # simulate impot v1 file to Aegis
    print('Begin import file to Aegis, file path:{}'.format(file_path))
    time.sleep(10)
    print('Finish')
