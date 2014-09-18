from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#

urlpatterns = patterns('',
	url(r'^index$', 'MyPeople.views.index'),
	url(r'^search_by_name$', 'MyPeople.views.search_by_name'),
	url(r'^add_friend$', 'MyPeople.views.add_friend'),
	url(r'^del_friend$', 'MyPeople.views.del_friend'),
	url(r'^get_friends$', 'MyPeople.views.get_friends'),
	url(r'^get_requests$', 'MyPeople.views.get_requests'),
	url(r'^accept_request$', 'MyPeople.views.accept_request'),
	url(r'^reject_request$', 'MyPeople.views.reject_request'),
)

