from django.contrib.auth.models import AbstractUser
from django.db import models
from blog.models import Ticket, Review


class User(AbstractUser):

    tickets_list = models.ManyToManyField(Ticket, related_name="tickets_list")
    reviews_list = models.ManyToManyField(Review, related_name="reviews_list")
    description = models.TextField(verbose_name="Description", max_length=1000, blank=True, null=True)


class UserFollows(models.Model):

    user_id = models.ForeignKey('User', related_name="following", on_delete=models.CASCADE)
    followed_user_id = models.ForeignKey('User', related_name="followers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'followed_user_id')

    def __str__(self):
        return f"{self.user_id}:{self.followed_user_id}"