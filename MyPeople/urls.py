from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#

urlpatterns = patterns('',
	url(r'^index$', 'MyPeople.views.index'),
	url(r'^searchByName$', 'MyPeople.views.searchByName'),
	url(r'^addFriend$', 'MyPeople.views.addFriend'),
	url(r'^delFriend$', 'MyPeople.views.delFriend'),
	url(r'^getFriends$', 'MyPeople.views.getFriends'),
	url(r'^getRequests$', 'MyPeople.views.getRequests'),
	url(r'^acceptRequest$', 'MyPeople.views.acceptRequest'),
	url(r'^rejectRequest$', 'MyPeople.views.rejectRequest'),
)

