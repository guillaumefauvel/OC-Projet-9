from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Review
from authentication.models import User, UserFollows
from django.contrib.auth.decorators import login_required
from . import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator


@login_required
def home(request):
    """ Redirect the user to the homepage. The page show the content of the people he follows.
     It also show his own content.
     """

    try:
        followers = UserFollows.objects.filter(user_id=request.user)
        user_object = User.objects.get(id=request.user.id)
        tickets = [ticket for ticket in user_object.tickets_list.all()]
        reviews = [review for review in user_object.reviews_list.all()]

        for user in followers:
            [tickets.append(ticket) for ticket in Ticket.objects.filter(user=user.followed_user_id)]
            [reviews.append(review) for review in Review.objects.filter(user=user.followed_user_id)]

        publications = set(tickets + reviews)
        publications = sorted(publications, key=lambda x: x.time_created, reverse=True)

    except ObjectDoesNotExist:

        publications = []
    paginator = Paginator(publications, 3)
    page_number = request.GET.get('page')
    publications_page_object = paginator.get_page(page_number)

    return render(request, 'home.html', context={'publications_page_object': publications_page_object})


@login_required
def ticket_list_view(request):
    """ Show the list of all the ticket created by the user. The ticket must be open/active. """

    ticket_objects = Ticket.objects.all()

    paginator = Paginator(ticket_objects, 8)
    page_number = request.GET.get('page')
    tickets_page_obj = paginator.get_page(page_number)

    context = {
        'tickets_page_obj': tickets_page_obj
    }
    return render(request, "tickets_reviews/ticket_list.html", context)


@login_required
def review_list_view(request):
    """ Show the list of all the published reviews """

    review_objects = Review.objects.all()

    paginator = Paginator(review_objects, 8)
    page_number = request.GET.get('page')
    review_page_objects = paginator.get_page(page_number)

    context = {
        'review_page_objects': review_page_objects
    }
    return render(request, "tickets_reviews/review_list.html", context)


@login_required
def show_review(request, review_id):
    """ Show the content of a selected review """

    review_object = Review.objects.get(id=review_id)

    return render(request, 'tickets_reviews/show_review.html', context={'review': review_object})


@login_required
def user_list(request):
    """ Show a list of all the users """

    search_error = False
    try:
        if request.GET['fname']:
            pass
        search_error = True
    except MultiValueDictKeyError:
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

    user_infos = sorted(user_infos.items(), key=lambda x: str(x[1]['user_object']), reverse=True)

    paginator = Paginator(user_infos, 6)
    page_number = request.GET.get('page')
    users_page_object = paginator.get_page(page_number)

    # print(user_infos[0][1]['user_object'])

    context = {
        'search_error': search_error,
        'users_page_object': users_page_object,
    }

    return render(request, "user/user_list.html", context)


@login_required
def profile(request):
    """ Show the profile of the current user. From here, he can change his password or update his description """

    user_name = request.user

    followings_number = len(UserFollows.objects.filter(user_id=user_name))
    followers_number = len(UserFollows.objects.filter(followed_user_id=user_name))

    context = {'user_name': user_name,
               'followings': followings_number,
               'followers': followers_number}

    return render(request, 'user/profile_view.html', context=context)


@login_required
def profile_tickets(request):
    """ Show the tickets of the current user. He can modify/delete those that are not closed yet """

    guest_tickets = Ticket.objects.filter(user=request.user)
    reviews = [review for review in Review.objects.all() if review.ticket is not False]

    context = {
        'item_list': guest_tickets,
        'review_list': reviews,
        'heading_one': 'Tickets ouverts',
        'empty_message': 'Je n\'ai pas encore ouvert de ticket',
        'page_ref': 'ticket-page',
        'delete_item': 'delete-ticket',
        'modify_item': 'modify-ticket',
    }

    return render(request, 'user/profile_list.html', context=context)


@login_required
def profile_reviews(request):
    """ Show the reviews published by the current user. He can modify and delete them """
    guest_reviews = Review.objects.filter(user=request.user)

    context = {
        'item_list': guest_reviews,
        'heading_one': 'Critiques publiées',
        'empty_message': 'Vous n\'avez pas encore publié de critique',
        'page_ref': 'show-review',
        'delete_item': 'delete-review',
        'modify_item': 'modify-review',
    }

    return render(request, 'user/profile_list.html', context=context)


@login_required
def user_page(request, user_id):
    """ Show the profile page of a given user. It shows the tickets he has open and his published review. """

    guest = get_object_or_404(User, id=user_id)
    tickets = Ticket.objects.filter(user=user_id)
    reviews = Review.objects.filter(user=user_id)

    try:
        relation = UserFollows.objects.get(user_id=request.user, followed_user_id=guest)
        action = 'unfollow'
    except ObjectDoesNotExist:
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
        'foreign_reviews': Review.objects.all(),
        'page_ref': 'ticket-page',
        'action': action,
        'followings': followings_number,
        'followers': followers_number,
    })


@login_required
def create_ticket(request):
    """ This is a form view that create a new ticket """

    ticket_form = forms.TicketCreationForm()
    if request.method == 'POST':
        ticket_form = forms.TicketCreationForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            user_object = User.objects.get(id=request.user.id)
            ticket.save()
            user_object.tickets_list.add(ticket)
            user_object.save()
            return redirect('ticket-list')

    context = {'form': ticket_form, 'item_type': 'un nouveau ticket'}

    return render(request, 'tickets_reviews/item_submission.html', context=context)


@login_required
def create_review(request):
    """ This is a form view that publish a review that is not related to a ticket """

    review_form = forms.ReviewCreationForm()

    if request.method == 'POST':
        review_form = forms.ReviewCreationForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            try:
                review.ticket = request.ticket
            except AttributeError:
                pass
            review.save()
            user_object = User.objects.get(id=request.user.id)
            user_object.reviews_list.add(review)
            user_object.save()
            return redirect('home')

    context = {'form': review_form, 'item_type': 'une nouvelle critique'}

    return render(request, 'tickets_reviews/item_submission.html', context=context)


@login_required
def review_from_ticket(request, ticket_id):
    """ This is a form view that publish a review is response to a given ticket """

    ticket = get_object_or_404(Ticket, id=ticket_id)

    try:
        Review.objects.get(ticket=ticket)
        return redirect('home')
    except ObjectDoesNotExist:
        pass

    review_form = forms.LinkedReviewForm()

    if request.method == 'POST':
        review_form = forms.LinkedReviewForm(request.POST)
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
            user_object = User.objects.get(id=request.user.id)
            user_object.reviews_list.add(review)
            user_object.save()

            return redirect('home')

    return render(request, 'tickets_reviews/ticket_page.html', context={'ticket_id': ticket, 'form': review_form})


@login_required
def delete_ticket(request, ticket_id):
    """ Check if the user is the author of the ticket, if it is the case it redirect the user to the delete confirmation page """

    ticket = get_object_or_404(Ticket, id=ticket_id)

    context = {'item_id': ticket_id,
               'item': ticket,
               'item_name': 'ce ticket',
               'deletion_path': 'confirm-delete-ticket'}

    if check_ownership(request, ticket):
        return render(request, 'tickets_reviews/item_deletion_confirmation.html', context)

    return render(request, 'access_denied.html')


@login_required
def confirm_deletion_ticket(request, ticket_id):
    """ Delete the selected ticket if the user is the author of it """

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if check_ownership(request, ticket):
        ticket.delete()
        return redirect('profile-tickets')

    return redirect('home')


@login_required
def modify_ticket(request, ticket_id):
    """ Show a prefilled form that the user can modify in order to update his ticket """

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not check_ownership(request, ticket):
        redirect('home')

    if request.method == 'POST':
        form = forms.TicketCreationForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('profile-tickets')
    else:
        form = forms.TicketCreationForm(instance=ticket)

    return render(request, 'tickets_reviews/item_update.html', {'form': form, 'heading': 'du ticket'})


@login_required
def modify_review(request, review_id):
    """ Show a prefilled form that the user can modify in order to update his review """

    review = get_object_or_404(Review, id=review_id)

    if not check_ownership(request, review):
        redirect('home')

    if request.method == 'POST':
        form = forms.ReviewCreationForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('profile-reviews')
    else:
        form = forms.ReviewCreationForm(instance=review)

    return render(request, 'tickets_reviews/item_update.html', {'form': form, 'heading': 'de la critique'})


def check_ownership(request, object_ref):
    """ Verify if the current user his the author of the selected object """
    if request.user == object_ref.user:
        return True
    return False


@login_required
def delete_review(request, review_id):
    """ Check if the user is the author of the review, if it is the case it redirect the user to the delete confirmation page """

    review = get_object_or_404(Review, id=review_id)

    context = {'item_id': review_id,
               'item': review,
               'item_name': 'cette critique',
               'deletion_path': 'confirm-delete-review'}

    if check_ownership(request, review):
        return render(request, 'tickets_reviews/item_deletion_confirmation.html', context)

    return render(request, 'access_denied.html')


@login_required
def confirm_deletion_review(request, review_id):
    """ Delete the selected review if the user is the author of it """

    review = get_object_or_404(Review, id=review_id)

    if check_ownership(request, review):
        review.delete()
        redirect('profile-reviews')
    return redirect('home')


@login_required
def follow(request, user_id):
    """ Create a follow relation between the current user and the selected one """

    user_object = User.objects.get(id=user_id)
    UserFollows.objects.create(user_id=request.user, followed_user_id=user_object)

    return redirect('user-page', user_id)


@login_required
def unfollow(request, user_id):
    """ Delete the follow relation between the current user and the selected one """

    user_object = User.objects.get(id=user_id)
    relation = UserFollows.objects.get(user_id=request.user, followed_user_id=user_object)
    relation.delete()

    return redirect('user-page', user_id)


@login_required
def manage_subscriptions(request):
    """ Show the subscriptions of the current user """

    followers = UserFollows.objects.filter(user_id=request.user.id)
    user_objects = []
    for value in followers:
        user_objects.append(User.objects.get(id=value.followed_user_id.id))

    return render(request, 'user/subscription_manager.html', context={'followers': user_objects})


@login_required
def unfollow_from_manager(request, user_id):
    """ Delete the follow relation between the current user and the selected one """

    user_object = User.objects.get(id=user_id)
    relation = UserFollows.objects.get(user_id=request.user, followed_user_id=user_object)
    relation.delete()

    return redirect('subscription-management')


@login_required
def search_user(request):
    """ Search in the database if the input correspond to a username, 
    if it does, it redirect the  current user to the user page """

    researched_user = request.GET['fname']
    try:
        researched_user = User.objects.get(username=researched_user)
    except ObjectDoesNotExist:
        return user_list(request)
    return redirect('user-page', researched_user.id)


@login_required
def add_description(request):
    """ Show a prefilled form that the user can modify in order to update his description """

    user_object = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = forms.AddDescription(request.POST, instance=user_object)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = forms.AddDescription(instance=user_object)

    return render(request, 'user/description_update.html', {'form': form, 'heading': 'de la description'})


@login_required
def show_authors(request):
    """ Show a list of the books authors"""

    tickets = Ticket.objects.all()
    reviews = Review.objects.all()

    authors_references = [item.content_author for item in tickets]
    authors_references.extend([item.content_author for item in reviews])
    authors_references = set(authors_references)
    authors_references = sorted(authors_references, key=lambda x: str(x.split()[1]) if (' ' in x) else str(x))

    return render(request, 'tickets_reviews/authors_list.html', context={'authors': authors_references})


@login_required
def show_author_work(request, author_refererence):
    """ Show a list of all the selected author's work """

    tickets = Ticket.objects.filter(content_author=author_refererence, status=True)
    reviews = Review.objects.filter(content_author=author_refererence)

    context = {
        'tickets': tickets,
        'reviews': reviews,
        'author': author_refererence,
    }

    return render(request, 'tickets_reviews/author_work.html', context=context)
