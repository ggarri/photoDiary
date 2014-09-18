from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseServerError
from django.template import Context
from django.views.decorators.csrf import csrf_exempt

from Photos.messages import MessageCode
from Photos.models import *

from Common.component.messages import MessageVO
from Common.component.UploadProgressHandler import *


def start(request, view):
    return render_to_response(view, {}, context_instance=Context(request))


def get_tmp_photos(request):
    user = User.objects.get(pk=request.session['logged']['id'])
    tmp = tmp_photo.objects.filter(owner=user)
    return render_to_response(request.GET['view'], {'Photos': tmp}, context_instance=Context(request))


def get_bound_photos(request):
    if request.method == "GET":
        user = User.objects.get(pk=request.session['logged']['id'])
        data = {'Photos': user.get_photos_by_bound(request.GET['ca_b'],
                                                request.GET['ca_j'],
                                                request.GET['ea_b'],
                                                request.GET['ea_j'])}
        return render_to_response(request.GET['view'], data, context_instance=Context(request))

    else:
        result = MessageVO(_type=False, msg=MessageCode._001)
        return HttpResponse(result.getJSON(), mimetype='application/json')


@csrf_exempt
def del_tmp_photo(request):
    if request.method == "POST":
        photo = tmp_photo.objects.get(pk=request.POST['id'])
        photo.delete()
    return HttpResponse()


@csrf_exempt
def add_tmp_photo(request):
    # Create a new temporal photo
    # request.upload_handlers.insert(0, UploadProgressHandler(request))
    for _file in request.FILES.getlist('files'):
        tmp_photo.create(img=_file, userId=request.session['logged']['id'])

    # Moving from coordiante photos to temporal ones
    if 'id' in request.POST:
        photo = Photo.objects.get(pk=request.POST['id'])
        photo.move_to_temp()

    return HttpResponse()


@csrf_exempt
def get_photo_by_id(request):
    if request.method == "GET":
        photo = Photo.objects.get(pk=request.GET['id'])
        return render_to_response(request.GET['view'], {'data': photo}, context_instance=Context(request))

    result = MessageVO(_type=False, msg=MessageCode._001)
    return HttpResponse(result.getJSON(), mimetype='application/json')

@csrf_exempt
def set_photo_by_id(request):
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
            return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')