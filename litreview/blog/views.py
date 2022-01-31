from django.shortcuts import render, redirect
from .models import Ticket
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')

def ticket_list_view(request):

    ticket_objects = Ticket.objects.all()

    context = {
        'ticket_objects': ticket_objects
    }
    return render(request, "ticket_list.html", context)


def create_ticket(request):
    ticket_form = forms.Ticket_Creation_Form()
    if request.method == 'POST':
        ticket_form = forms.Ticket_Creation_Form(request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.ticket_author = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'ticket_submission.html', context={'form': ticket_form})