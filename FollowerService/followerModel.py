from django.db import models
#the user instance will have to be obtained through an Api call 

class Follower(models.Model):
    user_id = models.IntegerField()  # get the ID of the user who is searching for a user to follow
    followerUserId = models.IntegerField()  # get the ID of the user being followed

    class Meta:
        unique_together = ('user_id', 'followerUserId')  # Prevent duplicate follows
