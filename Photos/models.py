from PIL import Image
from django.core.files import File
import StringIO
import os
import hashlib
import shutil
import time

from Map.models import *
from Users.models import *

from django.conf import settings

#--------------------------------------------------------
#		CLASS PHOTO
#--------------------------------------------------------


class Photo(models.Model):
    title = models.CharField(max_length=50, default="Insert title")
    img = models.ImageField(blank=True, upload_to="uploaded/photos/")
    width = models.FloatField(blank=False)
    height = models.FloatField(blank=False)
    comment = models.CharField(max_length=500, default="Insert comment")
    date = models.DateField(auto_now=True)
    coordinate = models.ForeignKey(Coordinate, null=True, blank=True, related_name="photos")

    @staticmethod
    def create(img, x=1, y=1):
        p = Photo(img=img, width=x, height=y)
        p.save()
        return p

    @staticmethod
    def get_by_bound(ca_b, ca_j, ea_b, ea_j):
        coordinates = Coordinate.get_by_bound(ca_b, ca_j, ea_b, ea_j);
        in_photos = list()
        for c in coordinates:
            for p in c.photos.all():
                in_photos.append(p)

        return in_photos

    def move_to_temp(self):
        file_name = os.path.basename(str(self.img))
        # print 'FROM :',settings.PHOTOS_ROOT+file_name
        # print 'TO :',settings.TMP_ROOT+file_name
        # print 'URL :',settings.TMP_URL+file_name
        shutil.copy(settings.PHOTOS_ROOT+file_name, settings.TMP_ROOT+file_name)
        new_photo = TmpPhoto(img=settings.TMP_URL+file_name, width=self.width
                             , height=self.height, owner=self.coordinate.owner)
        new_photo.save()
        # Save temporal
        # Delete old
        self.delete()

    def delete(self, *args, **kwargs):
        self.img.delete()
        super(Photo, self).delete(*args, **kwargs)


class TmpPhoto(models.Model):
    img = models.ImageField(blank=True, upload_to="uploaded/tmp/")
    width = models.FloatField(blank=False)
    height = models.FloatField(blank=False)
    owner = models.ForeignKey(User, related_name="TmpPhotos")

    @staticmethod
    def create(img, userId):
        def _resize(i, x, y):
            # read image from InMemoryUploadedFile
            strfile = ""
            for c in i.chunks():
                strfile += c

            # create PIL Image instance
            imagefile = StringIO.StringIO(strfile)
            image = Image.open(imagefile)
            print image.mode
            # if not RGB, convert
            if image.mode not in ("L", "RGB"):
                image = image.convert("RGB")

            #get orginal image ratio
            (width, height) = image.size[0], image.size[1]

            # get output with and height to do the first crop
            if width > x:
                new_width = x
                new_height = (float(height)/float(width)) * x
                # image = image.resize((new_width, new_height))
                image.thumbnail([new_width, new_height], Image.ANTIALIAS)
            elif height > y:
                new_height = y
                new_width = (float(width)/float(height)) * y
                # image = image.resize((new_width, new_height))
                image.thumbnail([new_width, new_height], Image.ANTIALIAS)
            else:
                new_height = height
                new_width = width


            # re-initialize imageFile and set a hash (unique file_name)
            imagefile = StringIO.StringIO()
            file_name = hashlib.md5(imagefile.getvalue()).hexdigest()
            file_name = file_name[1:10]+str(time.time())+'.jpg'

            #save to disk
            imagefile = open(os.path.join('/tmp',file_name), 'w')
            image.save(imagefile,'JPEG', quality=90)
            imagefile = open(os.path.join('/tmp',file_name), 'r')
            content = File(imagefile)

            return content, new_width, new_height

        owner = User.objects.get(pk=userId)

        imageImage = Image.open(img)
        (img2, width, height) = _resize(img, 1024, 960)
        p = TmpPhoto(img=img2, width=width, height=height, owner=owner)

        #p = TmpPhoto(img=img, width=imageImage.size[0], height=imageImage.size[1], owner=owner)
        p.save()
        return p

    def move_to_coor(self, userId, coorId):
        user = User.objects.get(pk=userId)
        coor = Coordinate.objects.filter(owner=user).get(pk=coorId)

        file_name = os.path.basename(str(self.img))
        # print 'FROM :',settings.TMP_ROOT+file_name
        # print 'TO :',settings.PHOTOS_ROOT+file_name
        # print 'URL :',settings.PHOTOS_URL+file_name
        shutil.copy(settings.TMP_ROOT+file_name, settings.PHOTOS_ROOT+file_name)
        new_photo = Photo(img=settings.PHOTOS_URL+file_name, width=self.width, height=self.height)
        # Save temporal
        new_photo.save()
        # Add photo to the coordinate
        coor.photos.add(new_photo)
        coor.save()
        self.delete() # Delete old

    def delete(self, *args, **kwargs):
        # self.img.delete()
        super(TmpPhoto, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(TmpPhoto, self).save(*args, **kwargs)

#--------------------------------------------------------
#		CLASS ALBUM
#--------------------------------------------------------
class Album(models.Model):
    pass

#--------------------------------------------------------
#		CLASS SLOT
#--------------------------------------------------------
class Slot(models.Model):
    pass