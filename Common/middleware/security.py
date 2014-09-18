from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from Users.models import *
import re


class AuthenticationUsers(object):

    # private_reg = re.compile('^\/map|photos|myPeople/*')
    # public_reg = re.compile('^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?')

    @staticmethod
    def process_request(request):
        # All images form media must be accept directly
        if request.path.startswith('/media/'):
            pass
        else:
            # Every part of app, lacking users menu
            if request.path.startswith('/map') or request.path.startswith('/photos') \
                    or request.path.startswith('/myPeople'):
                # Just logged users are able to access in app
                if 'logged' in request.session:
                    pass
                # Otherway, user has to identify himself
                else:
                    return HttpResponseRedirect('/')
            # Starting users menu
            else:
                if 'logged' in request.session:
                    # If user is logged, just it may logout
                    if request.path.endswith('logout'):
                        pass
                    # If user is logged and this tries to access this menu, redirect to...
                    else:
                        return HttpResponseRedirect('/map')
