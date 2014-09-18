from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import get_object_or_404, render_to_response

from django.views.generic import DetailView, ListView
from Map.models import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#

urlpatterns = patterns('Map.views', # Prefix for callback dispacher
    url(r'^$', 'start', {'view': 'Map/map.html'}),
    url(r'^get_coordinates$', 'get_coordinates'),
    # url(r'^get_coordinates$',
    #     ListView.as_view(
    #         queryset=Coordinate.objects.all(),
    #         context_object_name='data',
    #         template_name='Map/main.html')),
    url(r'^get_coordinate_by_id$', 'get_coordinate_by_id'),
    # url(r'^get_coordinate_by_id/(?P<pk>\d+)$',
    #     DetailView.as_view(
    #         model=Coordinate,
    #         template_name='Map/marker_form.html')),
    url(r'^get_coordinatesearch$', 'get_coordinatesearch'),
    url(r'^del_coordinate_photo$', 'del_coordinate_photo'),
    url(r'^set_coordinate_photo$', 'set_coordinate_photo'),
    url(r'^set_coordinate_title$', 'set_coordinate_title'),
    url(r'^set_coordinate$', 'set_coordinate'),
    url(r'^del_coordinate_by_id$', 'del_coordinate_by_id'),
    url(r'^get_coordinate_photos$', 'get_coordinate_photos'),
)
