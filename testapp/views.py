from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from celery_try import celery_app
from testapp import tasks
from .forms import SubmitForm
from celery.result import AsyncResult
import json
from celery.states import PENDING


def poll_state(request):
    """ A view to report the progress to the user """
    if request.is_ajax():
        if 'task_id' in request.POST and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
            print(data)
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    # avoid error crash
    json_data = {}
    if isinstance(data, str) or isinstance(data, list) or isinstance(data, dict):  # expired error
        if data == PENDING:
            json_data = json.dumps(dict(process_percent=0, state=PENDING))
        else:
            json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def index(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        context = {
            'task_id': job_id,
        }
        return render(request, "show_t.html", context)
    elif 'n' in request.GET:
        n = request.GET['n']
        # job = tasks.fib_list.apply_async((int(n),), expires=3600, queue='aegis_queue')
        # send tasks to remote worker
        job = celery_app.send_task('weaver_analysis', args=(int(n),), expires=3600, queue='aegis_queue')
        return HttpResponseRedirect(reverse('index') + '?job=' + job.id)
    else:
        form = SubmitForm()
        context = {
            'form': form,
        }
        return render(request, "post_form.html", context)
