from django import forms
from blog.models import Ticket, Review


class ticket_creation_form(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('content_reference', 'content_author', 'publication_year', 'user_comment', 'content_picture')


class review_creation_form(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content_reference', 'content_author', 'publication_year', 'rating', 'headline','body', 'content_picture')


class linked_review_form(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'headline','body')



