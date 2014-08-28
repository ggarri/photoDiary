from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.middleware.csrf import CsrfResponseMiddleware
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import serializers

from itertools import izip
import simplejson
import Image
import urllib
import ast
import shutil
import os
import time

from Users.messages import *
from Users.models import *
from Photos.models import *



#############################
#		Users Section		#
#############################

# Render index page with forms to register and identify users.
def start(request, view):
	return render_to_response(view, {} , context_instance=RequestContext(request) )

# Returns view with the form to register a new user
def getRegisterForm(request, view):
	return render_to_response(view, {'form': UserForm()} , context_instance=RequestContext(request) )	

def handler404(request):
	return HttpResponseRedirect(reverse('Users.views.start', kwargs={} ))	

@csrf_exempt
def login(request):
	if request.method == "POST":
		try:
			user = User.objects.get(nick=request.POST['nick'])
			if user.password == request.POST['password']:
				request.session['logged'] = {'nick': user.nick, 'id': user.id}
				result = MessageVO(_type=True, msg=MessageCode._101)
			else:
				result = MessageVO(_type=False, msg=MessageCode._103)
		except:
			result = MessageVO(_type=False, msg=MessageCode._104)
	else:
		result = MessageVO(_type=False, msg=MessageCode._001)

	return HttpResponse(result.getJSON(), mimetype='application/json')

# Create a new user in the app, using form user object
@csrf_exempt
def setNewUser(request):
	if request.method == "POST":
		user = UserForm(request.POST, auto_id=False)
		if user.is_valid():
			user.save()
			message = MessageVO(_type=True, msg=MessageCode._102)
		else:
			message = MessageVO(_type='error_form', exception=user.errors)
	else:
		message = MessageVO(_type=False, msg=MessageCode._101)

	return HttpResponse(message.getJSON(), mimetype='application/json')

@csrf_exempt
def logout(request):
	request.session.pop('logged')
	return HttpResponseRedirect(reverse('Users.views.start', kwargs={} ))