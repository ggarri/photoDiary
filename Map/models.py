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
	def getByBound(ca_b, ca_j, ea_b, ea_j):
		CA = Point(ca_b, ca_j)
		EA = Point(ea_b, ea_j)
		inCoordiantes = list()
		for c in Coordinate.objects.all():
			if min(CA.x, CA.y) < c.lat < max(CA.x, CA.y):
				if min(EA.x, EA.y) < c.lng < max(EA.x, EA.y):
						inCoordiantes.append(c)
		return inCoordiantes

	@staticmethod
	def getByBoundAndUser(user, ca_b, ca_j, ea_b, ea_j):
		CA = Point(ca_b, ca_j)
		EA = Point(ea_b, ea_j)
		inCoordiantes = list()
		for c in Coordinate.objects.filter(owner=user):
			if min(CA.x, CA.y) < c.lat < max(CA.x, CA.y):
				if min(EA.x, EA.y) < c.lng < max(EA.x, EA.y):
						inCoordiantes.append(c)
		return inCoordiantes


class Location(models.Model):
	address = models.CharField(max_length=200)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	cp = models.CharField(max_length=20)

	def composeAddress(self, items):
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