from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#

urlpatterns = patterns('',
	url(r'^index$', 'Users.views.start'),
	url(r'^setNewUser$', 'Users.views.setNewUser'),
	url(r'^getRegisterForm$', 'Users.views.getRegisterForm'),
	url(r'^login$', 'Users.views.login'),
	url(r'^logout$', 'Users.views.logout'),
)
