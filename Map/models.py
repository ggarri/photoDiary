from django.db import models

# Create your models here.

from Users.models import *

#--------------------------------------------------------
#		CLASS COORDINATE
#--------------------------------------------------------


class Coordinate(models.Model):
    title = models.CharField(max_length=50, default='Title Unknown')
    lat = models.FloatField(blank=False)
    lng = models.FloatField(blank=False)
    location = models.ForeignKey('Location', null=True, blank=True)
    icon = models.ImageField(blank=True, upload_to="uploaded/icon/")
    owner = models.ForeignKey(User, related_name="photos")

    @staticmethod
    def get_by_bound(ca_b, ca_j, ea_b, ea_j):
        ca = Point(ca_b, ca_j)
        ea = Point(ea_b, ea_j)
        in_coordiantes = list()
        for c in Coordinate.objects.all():
            if min(ca.x, ca.y) < c.lat < max(ca.x, ca.y):
                if min(ea.x, ea.y) < c.lng < max(ea.x, ea.y):
                    in_coordiantes.append(c)
        return in_coordiantes

    @staticmethod
    def get_by_bound_user(user, ca_b, ca_j, ea_b, ea_j):
        ca = Point(ca_b, ca_j)
        ea = Point(ea_b, ea_j)
        in_coordiantes = list()
        for c in Coordinate.objects.filter(owner=user):
            if min(ca.x, ca.y) < c.lat < max(ca.x, ca.y):
                if min(ea.x, ea.y) < c.lng < max(ea.x, ea.y):
                    in_coordiantes.append(c)
        return in_coordiantes


class Location(models.Model):
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    cp = models.CharField(max_length=20)

    def compose_address(self, items):
        for item in items:
            if "street_address" in item['types']:
                self.address = item['formatted_address']
            if "locality" in item['types']:
                self.city = item['formatted_address'].split(',')[0].strip()
            if "postal_code" in item['types']:
                self.cp = item['formatted_address'].split(',')[0].split()[0]
            if "country" in item['types']:
                self.country = item['formatted_address']


class Point():

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __unicode__(self):
        return "("+str(self.x)+","+str(self.y)+")"