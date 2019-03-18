from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import UserForm
from .tasks import fib_list
from celery.result import AsyncResult
import json


def poll_state(request):
    """ A view to report the progress to the user """
    if request.is_ajax():
        if 'task_id' in request.POST and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def index(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data': data,
            'task_id': job_id,
        }
        return render(request, "show_t.html", context)
    elif 'n' in request.GET:
        n = request.GET['n']
        job = fib_list.delay(int(n))
        return HttpResponseRedirect(reverse('index') + '?job=' + job.id)
    else:
        form = UserForm()
        context = {
            'form': form,
        }
        return render(request, "post_form.html", context)