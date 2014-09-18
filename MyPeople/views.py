from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import simplejson

from Users.models import *

#############################
#		My People			#
#############################
def index(request):
    return render_to_response('MyPeople/main.html', {} , context_instance=Context(request) )


def get_friends(request):
    user = User.objects.get(pk=request.session['logged']['id'])
    return render_to_response('MyPeople/friends.html', {'friends': user.friends.all()},
                              context_instance=Context(request))


def get_requests(request):
    user = User.objects.get(pk=request.session['logged']['id'])
    return render_to_response('MyPeople/requests.html', {'requests': user.requests.filter(pending=True)}
                              , context_instance=Context(request))

@csrf_exempt
def accept_request(request):
    user = User.objects.get(pk=request.session['logged']['id'])
    user.accept_request(request.POST['requestId'])
    return render_to_response('MyPeople/friends.html', {}, context_instance=Context(request) )

@csrf_exempt
def reject_request(request):
    user = User.objects.get(pk=request.session['logged']['id'])
    user.reject_request(request.POST['requestId'])
    return render_to_response('MyPeople/friends.html', {} , context_instance=Context(request) )


def search_by_name(request):
    name = request.GET['name']
    users = User.objects.filter(nick__icontains=name)
    return HttpResponse(serializers.serialize('json', users), mimetype='application/json')

@csrf_exempt
def add_friend(request):
    user = User.objects.get(pk=request.session['logged']['id'])
    if request.method == 'POST':
        user.add_request(request.POST['userId'])
        return HttpResponse({}, mimetype='application/json')
    return HttpResponse(simplejson.dumps({'result': False, 'description': "Incorrect method"})
                        , mimetype='application/json')

@csrf_exempt
def del_friend(request):
    user = User.objects.get(pk=request.session['logged']['id'])
    if request.method == 'POST':
        user.del_friend(request.POST['userId'])
        return HttpResponse({}, mimetype='application/json')
    return HttpResponse(simplejson.dumps({'result':False, 'description':"Incorrect method"})
                        , mimetype='application/json')