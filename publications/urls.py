from django.conf.urls.defaults import *
from publications import views

urlpatterns = patterns('',
    url(r'^latest/$', views.latest, name='pub_latest'),
    url(r'^create/$', views.create, name='pub_create'),
)
