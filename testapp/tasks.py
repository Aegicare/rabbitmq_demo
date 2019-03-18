from celery import shared_task, current_task


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
