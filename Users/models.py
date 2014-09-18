from django.db import models
from django.forms import ModelForm


class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    nick = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    friends = models.ManyToManyField('User', blank=True)
    requests = models.ManyToManyField('FriendRequest', blank=True, related_name='owner')

    def add_request(self, friend_id):
        friend = User.objects.get(pk=friend_id)
        # If the request was pending, it is activate again
        old_request = FriendRequest.objects.filter(user=friend)
        if len(old_request) > 0:
            old_request[0].pending = True
            old_request[0].save()
        else:
            request = FriendRequest(user=friend)
            request.save()
            self.requests.add(request)
        self.save()

    def get_photos_by_bound(self, ca_b, ca_j, ea_b, ea_j):
        from Map.models import *

        coordinates = Coordinate.get_by_bound_user(self, ca_b, ca_j, ea_b, ea_j);
        in_photos = list()
        for c in coordinates:
            for p in c.photos.all():
                in_photos.append(p)
        return in_photos

    def del_friend(self, friend_id):
        friend = self.friends.get(pk=friend_id)
        self.friends.remove(friend)
        self.save()

    def accept_request(self, request_id):
        request = self.requests.get(pk=request_id)
        self.friends.add(request.user)
        self.save()
        request.delete()

    def reject_request(self, request_id):
        request = self.requests.get(pk=request_id)
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
