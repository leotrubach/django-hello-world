from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django_hello_world.hello.views import (
    EditOwner, UpdateRequest, RequestList)

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'django_hello_world.hello.views.home', name='home'),
    url(r'^requests$',
        RequestList.as_view(),
        name='requests'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^edit_owner/(?P<pk>\d+)$', EditOwner.as_view(), name='edit_owner'),
    url(r'^update_request/(?P<pk>\d+)$',
        UpdateRequest.as_view(),
        name='update_request'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
    urlpatterns += staticfiles_urlpatterns()
