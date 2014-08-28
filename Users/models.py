from django.db import models
from django.forms import ModelForm

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=50)
	surname = models.CharField(max_length=100)
	email = models.CharField(max_length=200, unique=True)
	nick = models.CharField(max_length=20, unique=True)
	password = models.CharField(max_length=20)
	friends = models.ManyToManyField('User', blank=True)
	requests = models.ManyToManyField('FriendRequest', blank=True, related_name='owner')

	def addRequest(self, friendId):
		friend = User.objects.get(pk=friendId)
		# If the request was pending, it is activate again
		oldRequest = FriendRequest.objects.filter(user=friend)
		if len(oldRequest) > 0:
			oldRequest[0].pending = True
			oldRequest[0].save()
		else:
			request = FriendRequest(user=friend)
			request.save()
			self.requests.add(request)

		self.save()


	def getPhotosByBound(self, ca_b, ca_j, ea_b, ea_j):
		from Map.models import *

		coordinates = Coordinate.getByBoundAndUser(self, ca_b, ca_j, ea_b, ea_j);
		inPhotos = list();
		for c in coordinates:
			for p in c.photos.all():
				inPhotos.append(p)
		return inPhotos

	def delFriend(self, friendId):
		friend = self.friends.get(pk=friendId)
		self.friends.remove(friend)
		self.save()

	def acceptRequest(self, requestId):
		request = self.requests.get(pk=requestId)
		self.friends.add(request.user)
		self.save()
		request.delete()

	def rejectRequest(self, requestId):
		request = self.requests.get(pk=requestId)
		request.pending = False
		request.save()


class FriendRequest(models.Model): 
	user = models.ForeignKey('User', blank=True)
	date = models.DateField(auto_now=True)
	pending = models.BooleanField(default=True)



class UserForm(ModelForm):
	class Meta:
		model = User
		exclude = ('friends', 'requests')
