from __future__ import absolute_import
from test_celery.celery_app import app
import urllib.request
import os

# Where the downloaded files will be stored
BASEDIR = "E:/tmp/"


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


@app.task
def download(url, filename):
    """
    Download a page and save it to the BASEDIR directory
      url: the url to download
      filename: the filename used to save the url in BASEDIR
    """
    response = urllib.request.urlopen(url)
    data = response.read()
    with open(BASEDIR + "/" + filename, 'wb') as file:
        file.write(data)
    file.close()


@app.task
def list():
    """ Return an array of all downloaded files """
    return os.listdir(BASEDIR)


@app.task
def fib_yield(n):
    a, b = 0, 1
    while n > 0:
        yield b
        a, b = b, a + b
        n -= 1


@app.task
def fib_recursion(n):
    """ 故意让时间很长很长"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_recursion(n - 1) + fib_recursion(n - 2)
