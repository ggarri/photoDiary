from Photos.models import Photo, tmpPhoto
#from MagicController.models import MagicCombination
from django.contrib import admin


class PhotoAdmin(admin.ModelAdmin):
	model = Photo

        

admin.site.register(Photo, PhotoAdmin)
#admin.site.register(Recipe)

