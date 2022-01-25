from django.shortcuts import render
from .models import Ticket, Review, UserFollows

# Create your views here.
def index(request):
    return render(request, 'index.html')

def ticket_list_view(request):
    ticket_objects = Ticket.objects.all()

    context = {
        'ticket_objects': ticket_objects
    }
    return render(request, "ticket/ticket_list.html", context)

