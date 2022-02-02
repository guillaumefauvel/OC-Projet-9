from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Review
from authentication.models import User
from django.contrib.auth.decorators import login_required
from . import forms

import operator

@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def ticket_list_view(request):

    ticket_objects = Ticket.objects.all()

    context = {
        'ticket_objects': ticket_objects
    }
    return render(request, "ticket_list.html", context)


@login_required
def review_list_view(request):

    review_objects = Review.objects.all()

    context = {
        'review_objects': review_objects
    }
    return render(request, "review_list.html", context)

@login_required
def show_review(request, review_id):

    review_object = Review.objects.get(id=review_id)

    return render(request, 'show_review.html', context={'review': review_object} )

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
def profile_tickets(request):

    guest_tickets = Ticket.objects.filter(ticket_author=request.user)

    context = {
        'item_list': guest_tickets,
        'heading_one': 'Tickets ouverts',
        'empty_message': 'Je n\'ai pas encore ouvert de ticket',
    }

    return render(request, 'profile_list.html', context=context)


@login_required
def profile_reviews(request):

    guest_reviews = Review.objects.filter(user=request.user)

    context = {
        'item_list': guest_reviews,
        'heading_one': 'Critiques publiées',
        'empty_message': 'Vous n\'avez pas encore publié de critique',
    }

    return render(request, 'profile_list.html', context=context)


@login_required
def user_page(request, user_id):

    guest = get_object_or_404(User, id=user_id)

    ## TODO - Find Alternatives
    tickets = []
    for ticket in Ticket.objects.all():
        if user_id == ticket.ticket_author.id:
            tickets.append(ticket)
    reviews = []
    for review in Review.objects.all():
        if user_id == review.user.id:
            reviews.append(review)

    return render(request, 'user_page.html', context={'guest_id': guest, 'tickets': tickets, 'reviews': reviews})


@login_required
def create_ticket(request):

    ticket_form = forms.ticket_creation_form()
    if request.method == 'POST':
        ticket_form = forms.ticket_creation_form(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.ticket_author = request.user
            ticket.save()
            return redirect('ticket-list')
    return render(request, 'ticket_submission.html', context={'form': ticket_form})


@login_required
def create_review(request):
    """This is a review query which is not link to any ticket"""

    review_form = forms.review_creation_form()

    if request.method == 'POST':
        review_form = forms.review_creation_form(request.POST, request.FILES)
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


@login_required
def review_from_ticket(request, ticket_id):
    """This is a review query linked to a ticket"""

    ticket = get_object_or_404(Ticket, id=ticket_id)

    review_form = forms.linked_review_form()

    if request.method == 'POST':
        review_form = forms.linked_review_form(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            ticket = Ticket.objects.get(pk=ticket_id)
            ticket.status = False
            ticket.save()
            review.ticket = ticket
            review.content_reference = ticket.content_reference
            review.content_author = ticket.content_author
            review.content_picture = ticket.content_picture
            review.publication_year = ticket.publication_year
            review.save()

            return redirect('home')

    return render(request, 'ticket_page.html', context={'ticket_id': ticket, 'form': review_form})


@login_required
def subscribe(request, user_id):
    # TODO
    pass

@login_required
def delete_ticket(request, ticket_id):

    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except: # TODO Associer au type d'erreur
        return render(request, 'access_denied.html')

    if request.user == ticket.ticket_author:
        return render(request, 'item_deletion_confirmation.html', context={'ticket_id': ticket_id})
    else:
        return render(request, 'access_denied.html')


@login_required
def confirm_deletion_ticket(request, ticket_id):

    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except: # TODO Associer au type d'erreur
        return render(request, 'access_denied.html')

    ticket.delete()

    return redirect('home')


@login_required
def modify_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)
    #
    # if request.user == ticket.ticket_author:
    if request.method == 'POST':
        form = forms.ticket_creation_form(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('profile-tickets')
    else:
        form = forms.ticket_creation_form(instance=ticket)

    return render(request, 'ticket_update.html', {'form': form})

    # else:
    #     return render(request, 'access_denied.html')

@login_required
def delete_review(request, review_id):

    try:
        review = Review.objects.get(id=review_id)
    except: # TODO Associer au type d'erreur
        return render(request, 'home.html')

    if request.user == review.user:
        return render(request, 'item_deletion_confirmation.html', context={'review_id': review_id})
    else:
        return render(request, 'home.html')


@login_required
def confirm_deletion_review(request, review_id):

    try:
        review = Review.objects.get(id=review_id)
    except: # TODO Associer au type d'erreur
        return render(request, 'home.html')

    review.delete()

    return redirect('home')
