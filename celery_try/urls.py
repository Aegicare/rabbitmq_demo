from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='index')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', include('testapp.urls')),
]
