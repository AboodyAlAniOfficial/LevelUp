from django.contrib.auth.models import User
from django.db import models

class Followers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        db_table = 'followers'
        unique_together = (('user_id', 'following_id'),)

    def __str__(self):
        return f"{self.user_id.username} follows {self.following_id.username}"


