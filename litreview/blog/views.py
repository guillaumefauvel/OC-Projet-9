from django.shortcuts import render
from .models import Ticket, Review, UserFollows
from django.contrib.auth.decorators import login_required
from . import models


# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')

def ticket_list_view(request):

    ticket_objects = Ticket.objects.all()

    context = {
        'ticket_objects': ticket_objects
    }
    return render(request, "ticket/ticket_list.html", context)

