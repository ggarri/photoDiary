from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.middleware.csrf import CsrfResponseMiddleware
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import simplejson

from Users.models import *

#############################
#		My People			#
#############################



def index(request):
	return render_to_response('MyPeople/main.html', {} , context_instance=RequestContext(request) )


def getFriends(request):
	user = User.objects.get(pk=request.session['logged']['id'])
	return render_to_response('MyPeople/friends.html', {'friends': user.friends.all() } , context_instance=RequestContext(request) )

def getRequests(request):
	user = User.objects.get(pk=request.session['logged']['id'])
	return render_to_response('MyPeople/requests.html', {'requests': user.requests.filter(pending=True) } , context_instance=RequestContext(request) )

@csrf_exempt
def acceptRequest(request):
	user = User.objects.get(pk=request.session['logged']['id'])
	user.acceptRequest(request.POST['requestId'])
	return render_to_response('MyPeople/friends.html', {} , context_instance=RequestContext(request) )

@csrf_exempt
def rejectRequest(request):
	user = User.objects.get(pk=request.session['logged']['id'])
	user.rejectRequest(request.POST['requestId'])
	return render_to_response('MyPeople/friends.html', {} , context_instance=RequestContext(request) )

def searchByName(request):
	name = request.GET['name']
	users = User.objects.filter(nick__icontains=name)
	return HttpResponse(serializers.serialize('json', users), mimetype='application/json')

@csrf_exempt
def addFriend(request):
	user = User.objects.get(pk=request.session['logged']['id'])
	if request.method == 'POST':
		user.addRequest(request.POST['userId'])
		return HttpResponse({}, mimetype='application/json')
	return HttpResponse(simplejson.dumps({'result':False, 'description':"Incorrect method"}), mimetype='application/json')

@csrf_exempt
def delFriend(request):
	user = User.objects.get(pk=request.session['logged']['id'])
	print request.POST['userId']
	if request.method == 'POST':
		user.delFriend(request.POST['userId'])
		return HttpResponse({}, mimetype='application/json')
	return HttpResponse(simplejson.dumps({'result':False, 'description':"Incorrect method"}), mimetype='application/json')