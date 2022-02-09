from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
import datetime

class Ticket(models.Model):

    content_reference = models.CharField(verbose_name='Titre de la référence', max_length=80)
    content_author = models.CharField(verbose_name='Nom de l\'auteur', max_length=80)
    content_picture = models.ImageField(verbose_name='Image', upload_to='ticket', blank=True, null=True)
    publication_year = models.IntegerField(verbose_name='Date de publication',
                                           validators=[MinValueValidator(-400),MaxValueValidator(datetime.date.today().year+1)],
                                           blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    user_comment = models.TextField(verbose_name='Commentaire', max_length=300)
    status = models.BooleanField(default=True)
    time_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.content_reference

    def to_class_name(value):
        return value.__class__.__name__

    class Meta:
        ordering = ['-time_created']

class Review(models.Model):

    RATING_CHOICE = [(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5")]

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(verbose_name='Notes', choices=RATING_CHOICE)
    headline = models.CharField(verbose_name="Titre", max_length=128)
    body = models.TextField(verbose_name="Critique",max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    content_reference = models.CharField(verbose_name='Titre de la référence', max_length=80, blank=True, null=True)
    content_author = models.CharField(verbose_name='Nom de l\'auteur', max_length=80, blank=True, null=True)
    content_picture = models.ImageField(verbose_name='Image', upload_to='ticket', blank=True, null=True)
    publication_year = models.IntegerField(verbose_name='Date de publication',
                                           validators=[MinValueValidator(-400),MaxValueValidator(datetime.date.today().year+1)],
                                           blank=True, null=True)
    def __str__(self):
        return self.headline

    def to_class_name(value):
        return value.__class__.__name__

    class Meta:
        ordering = ['-time_created']