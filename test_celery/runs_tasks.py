import time
from test_celery.tasks import download, list

if __name__ == '__main__':
    result = download.delay('https://www.python.org/static/community_logos/python-logo-master-v3-TM.png',
                            'python-logo.png')
    # at this time, our task is not finished, so it will return False
    print('Task finished? ', result.ready())
    print('Task result: ', result.result)
    # sleep several seconds to ensure the task has been finished
    time.sleep(5)
    # now the task should be finished and ready method will return True
    print('Task finished? ', result.ready())
    print('Task result: ', result.result)

    r = list.delay()
    r.ready()
    print(r.get(timeout=1))
