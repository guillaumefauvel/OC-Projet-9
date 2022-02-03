from django.contrib import admin

# Register your models here.

from .models import Ticket, Review
from authentication.models import UserFollows

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)