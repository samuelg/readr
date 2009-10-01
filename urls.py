from django.conf.urls.defaults import *
from django.contrib import admin
import settings
from publications.views import latest

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^publications/', include('publications.urls')),
    (r'^auth/', include('auth.urls')),                       
    url(r'^$', latest),
)

# setup to server static files in development mode
if settings.DEBUG:
    if settings.MEDIA_URL.startswith("/"):
        media_url = settings.MEDIA_URL[1:]
        urlpatterns += patterns('',
            (r'^%s(?P<path>.*)$' % media_url, 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        )

