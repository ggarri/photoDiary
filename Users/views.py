from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context
from django.views.decorators.csrf import csrf_exempt

from Users.messages import *
from Photos.models import *


# Render index page with forms to register and identify users.
def start(request, view):
    return render_to_response(view, {}, context_instance=Context(request))


# Returns view with the form to register a new user
def get_register_form(request, view):
    return render_to_response(view, {'form': UserForm()}, context_instance=Context(request))


def handler404():
    return HttpResponseRedirect(reverse('Users.views.start', kwargs={}))


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
        except ValueError:
            result = MessageVO(_type=False, msg=MessageCode._104)
    else:
        result = MessageVO(_type=False, msg=MessageCode._001)

    return HttpResponse(result.getJSON(), mimetype='application/json')

# Create a new user in the app, using form user object
@csrf_exempt
def set_new_user(request):
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