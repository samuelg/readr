from django.conf.urls.defaults import *
from django.contrib.auth.views import login, redirect_to_login, logout
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^publications/', include('publications.urls'))
    #(r'^login/$',  login, {'template_name': 'login.html'}),
    #(r'^logout/$', logout),
    #(r'^pubs/$', ),
)
