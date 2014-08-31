from django.conf.urls import patterns, include, url, handler404
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#

from Users.models import *

handler404 = 'Users.views.handler404'
# Format (regular expression, Python callback function [, optional dictionary [, optional name]])
urlpatterns = patterns('Users.views',

    url(r'^$', 'start', {'view':'users.html'}),
    url(r'^setNewUser$', 'setNewUser'),
    url(r'^getRegisterForm$', 'getRegisterForm', {'view':'view/register.html'}),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),

    url(r'^map/', include('Map.urls')),
    url(r'^photos/', include('Photos.urls')),
    url(r'^myPeople/', include('MyPeople.urls')),

#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)