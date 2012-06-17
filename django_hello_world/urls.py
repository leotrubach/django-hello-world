from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'django_hello_world.hello.views.home', name='home'),
    url(r'^last_requests$',
        'django_hello_world.hello.views.last_ten_requests',
        name='last_requests'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
