import time
from test_celery.tasks import download, list, fib_recursion


def do_download():
    result = download.delay('https://www.python.org/static/community_logos/python-logo-master-v3-TM.png',
                            'python-logo.png')
    return result


def do_list():
    r = list.delay()
    r.ready()
    print(r.get(timeout=1))


def do_fib():
    result = fib_recursion.delay(30)
    return result


if __name__ == '__main__':
    # result = do_download()
    result = do_fib()
    # at this time, our task is not finished, so it will return False
    print('Task finished? ', result.ready())
    print('Task result: ', result.result)
    # sleep several seconds to ensure the task has been finished
    time.sleep(30)
    # now the task should be finished and ready method will return True
    print('Task finished? ', result.ready())
    print('Task result: {}'.format(result.result))
    print(result.result)
