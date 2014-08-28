from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import serializers

from itertools import izip
import simplejson
import urllib
import ast
import shutil
import os
import time
import string

# Own models
from Map.messages import *
from Photos.models import *


# @login_required
@csrf_exempt
def start(request, view):
	return render_to_response(view, {} , context_instance=Context(request) )

def getCoordinates(request):
	user = User.objects.get(pk=request.session['logged']['id'])
	data = [ coor for coor in Coordinate.objects.filter(owner=user).values('lat','lng', 'id', 'title')]
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def getCoordinateById(request):
	if request.method == "GET":
		user = User.objects.get(pk=request.session['logged']['id'])
		coor_info = Coordinate.objects.filter(owner=user).get(pk=request.GET['id'])
		return render_to_response(request.GET['view'], {'data': coor_info} , context_instance=Context(request) )
	else:
		result = MessageVO(_type=True, msg=MessageCode._001)
		return HttpResponse(result.getJSON(), mimetype='application/json')

@csrf_exempt
def setCoordinate(request):
	def getLocation():
		latlng = "%s,%s" % (request.POST['lat'],request.POST['lng'])
		url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=%s&sensor=%s" % (latlng, 'true')	
		address = ast.literal_eval(urllib.urlopen(url).read())
		if address['status'] == 'OK':
			loc = Location()
			loc.composeAddress(address['results'])
			return loc
		return None

	if request.method == "POST":
		# Updating location from stored coordinate which is identified by ID
		if 'id' in request.POST: 
			coor = Coordinate.objects.get(pk=request.POST['id'])
			coor.lat = request.POST['lat']
			coor.lng = request.POST['lng']
				
		# Creating a new coordinate
		else:
			user = User.objects.get(pk=request.session['logged']['id'])
			coor = Coordinate(lat=request.POST['lat'], lng=request.POST['lng'], owner=user)
			
		# Assigning location to the coordinate
		loc = getLocation()
		if loc != None:
			loc.save()
			coor.location = loc
			coor.save()
			result = simplejson.dumps({'id':coor.id})
		else:
			result = MessageVO(_type=False, msg=MessageCode._203).getJSON()
	else:
		result = MessageVO(_type=False, msg=MessageCode._001).getJSON()

	return HttpResponse(result, mimetype='application/json')

def getCoordinateSearch(request):
	if checkRequest(request, 'GET', ['name']):
		name = urllib.quote_plus(request.GET['name'])
		url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=%s" % (name, 'true')
		result = urllib.urlopen(url).read()
	else:
		result = MessageVO(_type=False, msg=MessageCode._204).getJSON()
	return HttpResponse(result, mimetype='application/json')



@csrf_exempt
def setCoordinatePhoto(request):
	if request.method == 'POST':
		tmp = tmpPhoto.objects.get(pk=request.POST['id'])
		tmp.moveToCoor(request.session['logged']['id'], request.POST['coordinateId'])
		result = MessageVO(_type=True, msg=MessageCode._201)
	else:
		result = MessageVO(_type=False, msg=MessageCode._001)
	return HttpResponse(result.getJSON(), mimetype='application/json')	


@csrf_exempt
def setCoordinateTitle(request):
	if request.method  == 'POST':
		user = User.objects.get(pk=request.session['logged']['id'])
		coor = Coordinate.objects.filter(owner=user).get(pk=request.POST['id'])
		coor.title = request.POST['title']
		coor.save()
		result = MessageVO(_type=True, msg=MessageCode._205)
	else:
		result = MessageVO(_type=False, msg=MessageCode._001)
	return HttpResponse(result.getJSON(), mimetype='application/json')	

@csrf_exempt
def delCoordinateById(request):
	if request.method == "POST":
		user = User.objects.get(pk=request.session['logged']['id'])
		coor = Coordinate.objects.filter(owner=user).get(pk=request.POST['id'])
		_id = coor.id
		coor.delete()
		result = simplejson.dumps({'id': _id})
	else:
		result = MessageVO(_type=False, msg=MessageCode._001).getJSON()
	return HttpResponse(result, mimetype='application/json')	
	


def getCoordinatePhotos(request):
	if request.method == "GET":
		user = User.objects.get(pk=request.session['logged']['id'])
		coor = Coordinate.objects.filter(owner=user).get(pk=request.GET['coordinateId'])
		if 'view' in request.GET: # Using a view to render them
			return render_to_response(request.GET['view'], {'Photos' : coor.photos.all()}, context_instance=Context(request) )
		else: # Return them to be rendered in the view
			data = [ p for p in coor.photos.values('id')]
			return HttpResponse(simplejson.dumps(data), mimetype='application/json')
	else:
		result = MessageVO(_type=False, msg=MessageCode._001).getJSON()
	return HttpResponse(result, mimetype='application/json')
	# else:
	# 	data = [ p for p in coor.photos.values('id')]
	# 	return HttpResponse(simplejson.dumps(data), mimetype='application/json')



@csrf_exempt
def delCoordinatePhoto(request):
	if request.method == 'POST':
		coor = Coordinate.objects.get(pk=request.POST['coordinateId'])
		photo = coor.photos.get(pk=request.POST['id'])
		coor.photos.remove(photo)
		coor.save()
		photo.delete()
		result = MessageVO(_type=False, msg=MessageCode._206)
	else:
		result = MessageVO(_type=False, msg=MessageCode._001)
	return HttpResponse(result.getJSON(), mimetype='application/json')