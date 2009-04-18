from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
import views

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^publications/', include('publications.urls')),
    url(r'^$', views.login_user, name='login'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^logout/$', views.logout_user, name='logout'),
)
