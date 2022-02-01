from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):

    content_reference = models.CharField('Titre de la référence', max_length=80)
    content_author = models.CharField('Nom de l\'auteur', max_length=80)
    content_picture = models.ImageField('Image', upload_to='ticket', blank=True, null=True)
    ticket_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    user_comment = models.TextField('Commentaire', max_length=300)
    status = models.BooleanField(default=True)
    time_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.content_reference


class Review(models.Model):

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    content_reference = models.CharField('Titre de la référence', max_length=80, blank=True, null=True)
    content_author = models.CharField('Nom de l\'auteur', max_length=80, blank=True, null=True)
    content_picture = models.ImageField('Image', upload_to='ticket', blank=True, null=True)

    def __str__(self):
        return self.headline


class UserFollows(models.Model):
    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs

        # user_object = ""
        # following = []
        # followers = []

        pass
        # unique_together = ('user', 'followed_user', )

