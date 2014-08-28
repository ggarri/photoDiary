from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.middleware.csrf import CsrfResponseMiddleware
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import serializers
from django.core.cache import cache

from itertools import izip
import simplejson
import Image
import urllib
import ast
import os
import time

from Photos.messages import *
from Photos.models import *
from common.UploadProgressHandler import *


def start(request, view):
	return render_to_response(view, {} , context_instance=RequestContext(request) )

def getTmpPhotos(request):
	user = User.objects.get(pk=request.session['logged']['id'])
	tmpP = tmpPhoto.objects.filter(owner=user)
	return render_to_response(request.GET['view'], { 'Photos' : tmpP } , context_instance=RequestContext(request) )

def getBoundPhotos(request):
	if request.method == "GET":
		user = User.objects.get(pk=request.session['logged']['id'])
		data = { 'Photos' : user.getPhotosByBound(request.GET['ca_b'], request.GET['ca_j'], request.GET['ea_b'], request.GET['ea_j']) }
		return render_to_response(request.GET['view'], data , context_instance=RequestContext(request) )
	else:
		result = MessageVO(_type=False, msg=MessageCode._001)
		return HttpResponse(result.getJSON(), mimetype='application/json')

@csrf_exempt
def delTmpPhoto(request):
	if request.method == "POST":
		photo = tmpPhoto.objects.get(pk=request.POST['id'])
		photo.delete()
	return HttpResponse()

@csrf_exempt
def addTmpPhoto(request):
	# Create a new temporal photo
	
	# request.upload_handlers.insert(0, UploadProgressHandler(request))

	for name in request.FILES:
		for _file in request.FILES.getlist('files'):
			tmpPhoto.create(img=_file, userId=request.session['logged']['id'])

	# Moving from coordiante photos to temporal ones
	if 'id' in request.POST:
		photo = Photo.objects.get(pk=request.POST['id'])
		photo.moveToTemp()

	return HttpResponse()

@csrf_exempt
def getPhotoById(request):
	if request.method == "GET":
		photo = Photo.objects.get(pk=request.GET['id'])
		return render_to_response(request.GET['view'], {'data': photo} , context_instance=RequestContext(request) )
	else:
		result = MessageVO(_type=False, msg=MessageCode._001)
		return HttpResponse(result.getJSON(), mimetype='application/json')

@csrf_exempt
def setPhotoById(request):
	if request.method == "POST":
		photo = Photo.objects.get(pk=request.POST['id'])
		photo.comment = request.POST['comment']
		photo.title = request.POST['title']
		photo.save()
		result = MessageVO(_type=True, msg=MessageCode._301)
	else:
		result = MessageVO(_type=False, msg=MessageCode._001)
	return HttpResponse(result.getJSON(), mimetype='application/json')


def upload_progress(request):
        """
        A view to report back on upload progress.
        Return JSON object with information about the progress of an upload.

        Copied from:
        http://djangosnippets.org/snippets/678/

        See upload.py for file upload handler.
        """
        #import ipdb
        #ipdb.set_trace()
        progress_id = ''
        if 'X-Progress-ID' in request.GET:
            progress_id = request.GET['X-Progress-ID']
        elif 'X-Progress-ID' in request.META:
            progress_id = request.META['X-Progress-ID']
        if progress_id:
            from django.utils import simplejson
            cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
            data = cache.get(cache_key)
            return HttpResponse(simplejson.dumps(data))
        else:
            return HttpResponseServerError(
                'Server Error: You must provide X-Progress-ID header or query param.')