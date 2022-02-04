from django.contrib import admin

# Register your models here.

from .models import Ticket, Review
from authentication.models import UserFollows, User

admin.site.register(UserFollows)
admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Review)
