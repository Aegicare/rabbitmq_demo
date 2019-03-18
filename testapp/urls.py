from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^poll_state$', views.poll_state, name='poll_state'),
]
