from django import forms
from blog.models import Ticket, Review
from authentication.models import User


class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('content_reference', 'content_author', 'publication_year', 'user_comment', 'content_picture')


class ReviewCreationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content_reference', 'content_author', 'publication_year',
                  'rating', 'headline', 'body', 'content_picture')


class LinkedReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'headline', 'body')


class AddDescription(forms.ModelForm):
    class Meta:
        model = User
        fields = ('description',)