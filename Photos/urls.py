from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#

urlpatterns = patterns('Photos.views',
	url(r'^$', 'start', {'view':'Public/view/galery.html'}),
    url(r'^addTmpPhoto$', 'addTmpPhoto'),
    url(r'^get_tmp_photos$', 'get_tmp_photos'),
    url(r'^delTmpPhoto$', 'delTmpPhoto'),
    url(r'^getBoundPhotos$', 'getBoundPhotos'),
    url(r'^getPhotoById$', 'getPhotoById'),
    url(r'^setPhotoById$', 'setPhotoById'),
    url(r'^upload_progress/$', 'upload_progress', name="admin-upload-progress")
)
