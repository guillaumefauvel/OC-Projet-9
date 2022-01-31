from django import forms
from blog.models import Ticket, Review

class Ticket_Creation_Form(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('content_reference', 'content_author', 'user_comment', 'content_picture')

class Review_Creation_Form(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'headline','body')
