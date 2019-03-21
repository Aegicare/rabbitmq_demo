import time

from celery import shared_task, current_task
from celery.result import AsyncResult


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


@shared_task
def import_analysis_result(file_path):
    # simulate impot v1 file to Aegis
    print('Begin import file to Aegis, file path:{}'.format(file_path))
    time.sleep(10)
    print('Finish')
