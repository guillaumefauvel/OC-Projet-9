from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    profile_photo = models.ImageField(verbose_name='photo de profil')


class UserFollows(models.Model):

    user_id = models.ForeignKey('User', related_name="following", on_delete=models.CASCADE)
    followed_user_id = models.ForeignKey('User', related_name="followers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'followed_user_id')

    def __str__(self):
        return f"{self.user_id}:{self.followed_user_id}"