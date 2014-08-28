from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
 	
from Users.models import *
import re

class authenticationUsers(object):

	# private_reg = re.compile('^\/map|photos|myPeople/*')
	# public_reg = re.compile('^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?')

    def process_request(self, request):
    	# All resources form media must be accept directly
    	if request.path.startswith('/media/'):
    		pass
    	else:
    		# Every part of app, lacking users menu
    		if request.path.startswith('/map') or request.path.startswith('/photos') or request.path.startswith('/myPeople'):
    			if 'logged' in request.session: # Just logged users are able to access in app
    				pass
    			else: # Otherway, user has to identify himself
    				return HttpResponseRedirect('/')
    		# Starting users menu
    		else: 
				if 'logged' in request.session:
					if request.path.endswith('logout'): # If user is logged, just it may logout
						pass
					else: # If user is logged and this tries to access this menu, redirect to...
						return HttpResponseRedirect('/map')
			