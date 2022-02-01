from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Review
from authentication.models import User
from django.contrib.auth.decorators import login_required
from . import forms

import operator
# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def ticket_list_view(request):

    ticket_objects = Ticket.objects.all()
    ticket_objects = sorted(ticket_objects, key=operator.attrgetter('time_created'), reverse=True)

    context = {
        'ticket_objects': ticket_objects
    }
    return render(request, "ticket_list.html", context)


@login_required
def ticket_page(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_page.html', context={'ticket_id': ticket})


@login_required
def review_list_view(request):

    review_objects = Review.objects.all()
    review_objects = sorted(review_objects, key=operator.attrgetter('time_created'), reverse=True)

    context = {
        'review_objects': review_objects
    }
    return render(request, "review_list.html", context)


@login_required
def user_list(request):

    user_objects = User.objects.all()

    context = {
        'user_objects': user_objects
    }
    return render(request, "user_list.html", context)


@login_required
def profile(request):

    user_name = request.user

    return render(request, 'profile_view.html', context={'user_name': user_name})


@login_required
def user_page(request, user_id):

    guest = get_object_or_404(User, id=user_id)

    return render(request, 'user_page.html', context={'guest_id': guest})


@login_required
def create_ticket(request):

    ticket_form = forms.Ticket_Creation_Form()
    if request.method == 'POST':
        ticket_form = forms.Ticket_Creation_Form(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.ticket_author = request.user
            ticket.save()
            return redirect('ticket-list')
    return render(request, 'ticket_submission.html', context={'form': ticket_form})


@login_required
def create_review(request):

    review_form = forms.Review_Creation_Form()
    if request.method == 'POST':
        review_form = forms.Review_Creation_Form(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            try:
                review.ticket = request.ticket
            except AttributeError:
                pass
            review.save()
            return redirect('home')
    return render(request, 'review_submission.html', context={'form': review_form})