from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#

urlpatterns = \
    patterns('Photos.views',
             url(r'^$', 'start', {'view': 'Public/view/galery.html'}),
             url(r'^add_tmp_photo$', 'add_tmp_photo'),
             url(r'^get_tmp_photos$', 'get_tmp_photos'),
             url(r'^del_tmp_photo$', 'del_tmp_photo'),
             url(r'^get_bound_photos$', 'get_bound_photos'),
             url(r'^get_photo_by_id$', 'get_photo_by_id'),
             url(r'^set_photo_by_id$', 'set_photo_by_id'),
             url(r'^upload_progress/$', 'upload_progress', name="admin-upload-progress")
)
