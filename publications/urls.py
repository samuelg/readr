from django.conf.urls.defaults import *
from publications import views

urlpatterns = patterns('',
    (r'^latest/$', views.latest),
)
