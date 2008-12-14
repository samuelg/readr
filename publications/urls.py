from django.conf.urls.defaults import *
from publications import views

urlpatterns = patterns('',
    url(r'^latest/$', views.latest, name='pub_latest'),
    url(r'^create/$', views.create, name='pub_create'),
    url(r'^read/(?P<publication_id>\d+)/$', views.read, name='pub_read'),
    url(r'^view/(?P<publication_id>\d+)/$', views.view, name='pub_view'),
)
