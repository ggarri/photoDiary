from django.conf.urls.defaults import patterns, include, url
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
    url(r'^getCoordinates$', 'getCoordinates'),
    # url(r'^getCoordinates$', 
    #     ListView.as_view(
    #         queryset=Coordinate.objects.all(),
    #         context_object_name='data',
    #         template_name='Map/main.html')),
    url(r'^getCoordinateById$', 'getCoordinateById'),
    # url(r'^getCoordinateById/(?P<pk>\d+)$',
    #     DetailView.as_view(
    #         model=Coordinate,
    #         template_name='Map/marker_form.html')),
    url(r'^getCoordinateSearch$', 'getCoordinateSearch'),
    url(r'^delCoordinatePhoto$', 'delCoordinatePhoto'),
    url(r'^setCoordinatePhoto$', 'setCoordinatePhoto'),
    url(r'^setCoordinateTitle$', 'setCoordinateTitle'),
    url(r'^setCoordinate$', 'setCoordinate'),
    url(r'^delCoordinateById$', 'delCoordinateById'),
    url(r'^getCoordinatePhotos$', 'getCoordinatePhotos'),
)
