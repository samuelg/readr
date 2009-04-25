from django.conf.urls.defaults import *
from django.contrib import admin
import settings
import views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^publications/', include('publications.urls')),
    url(r'^$', views.login_user, name='login'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^logout/$', views.logout_user, name='logout'),
)

# setup to server static files in development mode
if settings.DEBUG:
    if settings.MEDIA_URL.startswith("/"):
        media_url = settings.MEDIA_URL[1:]
        urlpatterns += patterns('',
            (r'^%s(?P<path>.*)$' % media_url, 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        )

