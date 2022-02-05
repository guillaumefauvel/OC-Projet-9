from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Review
from authentication.models import User, UserFollows
from django.contrib.auth.decorators import login_required
from . import forms
from django.http import HttpResponse

@login_required
def home(request):

    try:

        followers = UserFollows.objects.filter(user_id=request.user)
        tickets = []
        reviews = []

        for user in followers:
            try:
                for ticket in Ticket.objects.filter(user=user.followed_user_id):
                    tickets.append(ticket)
            except: # TODO Implement DoestNotExist
                pass

            try:
                for review in Review.objects.filter(user=user.followed_user_id):
                    reviews.append(review)
            except: # TODO Implement DoestNotExist
                pass

        publications = tickets + reviews
        publications = sorted(publications, key=lambda x: x.time_created, reverse=True)

    except: # TODO Implement DoestNotExist
        publications = []

    return render(request, 'home.html', context={'publications': publications})


@login_required
def ticket_list_view(request):

    ticket_objects = Ticket.objects.all()

    context = {
        'ticket_objects': ticket_objects
    }
    return render(request, "tickets_reviews/ticket_list.html", context)


@login_required
def review_list_view(request):

    review_objects = Review.objects.all()

    context = {
        'review_objects': review_objects
    }
    return render(request, "tickets_reviews/review_list.html", context)

@login_required
def show_review(request, review_id):

    review_object = Review.objects.get(id=review_id)

    return render(request, 'tickets_reviews/show_review.html', context={'review': review_object} )


@login_required
def user_list(request):

    search_error = False
    try:
        if request.GET['fname']:
            pass
        search_error = True
    except: # TODO Find the exception error
        pass

    user_infos = {}
    for author in User.objects.all():
        user_infos[author.id] = {
            'user_object': author,
            'ticket_number': len(Ticket.objects.filter(user=author)),
            'review_number': len(Review.objects.filter(user=author)),
            'follower_number': len(UserFollows.objects.filter(followed_user_id=author)),
            'following_number': len(UserFollows.objects.filter(user_id=author)),
        }

    context = {
        'search_error': search_error,
        'user_infos': user_infos,
    }

    return render(request, "user/user_list.html", context)


@login_required
def profile(request):

    user_name = request.user

    followings_number = len(UserFollows.objects.filter(user_id=user_name))
    followers_number = len(UserFollows.objects.filter(followed_user_id=user_name))

    context = {'user_name': user_name,
               'followings':followings_number,
               'followers': followers_number,}

    return render(request, 'user/profile_view.html', context=context)


@login_required
def profile_tickets(request):

    guest_tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.all()

    context = {
        'item_list': guest_tickets,
        'review_list': reviews,
        'heading_one': 'Tickets ouverts',
        'empty_message': 'Je n\'ai pas encore ouvert de ticket',
        'page_ref':'ticket-page',
        'delete_item': 'delete-ticket',
        'modify_item': 'modify-ticket',
    }

    return render(request, 'user/profile_list.html', context=context)


@login_required
def profile_reviews(request):

    guest_reviews = Review.objects.filter(user=request.user)

    context = {
        'item_list': guest_reviews,
        'heading_one': 'Critiques publiées',
        'empty_message': 'Vous n\'avez pas encore publié de critique',
        'page_ref':'show-review',
        'delete_item': 'delete-review',
        'modify_item': 'modify-review',
    }

    return render(request, 'user/profile_list.html', context=context)


@login_required
def user_page(request, user_id):

    guest = get_object_or_404(User, id=user_id)
    tickets = Ticket.objects.filter(user=user_id)
    reviews = Review.objects.filter(user=user_id)

    try:
        relation = UserFollows.objects.get(user_id=request.user, followed_user_id=guest)
        action = 'unfollow'
    except: # TODO DoestNotExit alternative
        if guest.id != request.user.id:
            action = 'follow'
        else:
            action = 'self'

    followings_number = len(UserFollows.objects.filter(user_id=guest))
    followers_number = len(UserFollows.objects.filter(followed_user_id=guest))

    return render(request, 'user/user_page.html', context={
        'guest_id': guest,
        'tickets': tickets,
        'reviews': reviews,
        'page_ref': 'ticket-page',
        'action': action,
        'followings': followings_number,
        'followers': followers_number,
    })


@login_required
def create_ticket(request):

    ticket_form = forms.ticket_creation_form()
    if request.method == 'POST':
        ticket_form = forms.ticket_creation_form(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket-list')

    context = {'form': ticket_form, 'item_type': 'un nouveau ticket'}

    return render(request, 'tickets_reviews/item_submission.html', context=context)


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

    context = {'form': review_form, 'item_type': 'une nouvelle critique'}

    return render(request, 'tickets_reviews/item_submission.html', context=context)


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

    return render(request, 'tickets_reviews/ticket_page.html', context={'ticket_id': ticket, 'form': review_form})


@login_required
def delete_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)

    context = {'item_id': ticket_id,
               'item_name': 'ce ticket',
               'deletion_path': 'confirm-delete-ticket'}

    if check_ownership(request, ticket):
        return render(request, 'tickets_reviews/item_deletion_confirmation.html', context)
    return render(request, 'access_denied.html')


@login_required
def confirm_deletion_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if check_ownership(request, ticket):
        ticket.delete()
        return redirect('profile-tickets')

    return redirect('home')


@login_required
def modify_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not check_ownership(request, ticket):
        redirect('home')

    if request.method == 'POST':
        form = forms.ticket_creation_form(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('profile-tickets')
    else:
        form = forms.ticket_creation_form(instance=ticket)

    return render(request, 'tickets_reviews/item_update.html', {'form': form, 'heading':'du ticket'})


@login_required
def modify_review(request, review_id):

    review = get_object_or_404(Review, id=review_id)

    if not check_ownership(request, review):
        redirect('home')

    if request.method == 'POST':
        form = forms.review_creation_form(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('profile-reviews')
    else:
        form = forms.review_creation_form(instance=review)

    return render(request, 'tickets_reviews/item_update.html', {'form': form, 'heading':'de la critique'})


def check_ownership(request, object):

    if request.user == object.user:
        return True

    return False

@login_required
def delete_review(request, review_id):

    review = get_object_or_404(Review, id=review_id)

    context = {'item_id': review_id,
               'item_name': 'cette critique',
               'deletion_path':'confirm-delete-review'}

    if check_ownership(request, review):
        return render(request, 'tickets_reviews/item_deletion_confirmation.html', context)
    return render(request, 'access_denied.html')


@login_required
def confirm_deletion_review(request, review_id):

    review = get_object_or_404(Review, id=review_id)

    if check_ownership(request, review):
        review.delete()
        redirect('profile-reviews')
    return redirect('home')


@login_required
def follow(request, user_id):

    user_object = User.objects.get(id=user_id)
    UserFollows.objects.create(user_id=request.user, followed_user_id=user_object)

    return redirect('user-page', user_id)


@login_required
def unfollow(request, user_id):

    user_object = User.objects.get(id=user_id)
    relation = UserFollows.objects.get(user_id=request.user, followed_user_id=user_object)
    relation.delete()

    return redirect('user-page', user_id)


@login_required
def manage_subscriptions(request):

    followers = UserFollows.objects.filter(user_id=request.user.id)
    user_objects = []
    for value in followers:
        user_objects.append(User.objects.get(id=value.followed_user_id.id))

    return render(request, 'user/subscription_manager.html', context={'followers': user_objects})


@login_required
def unfollow_from_manager(request, user_id):

    user_object = User.objects.get(id=user_id)
    relation = UserFollows.objects.get(user_id=request.user, followed_user_id=user_object)
    relation.delete()

    return redirect('subscription-management')

@login_required
def search_user(request):

    researched_user = request.GET['fname']
    try:
        researched_user = User.objects.get(username=researched_user)
    except:
        return user_list(request)
    return redirect('user-page', researched_user.id)

