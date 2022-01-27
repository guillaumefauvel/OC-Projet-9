from django import forms
from models import Ticket, Review

class Ticket_Creation_Form(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('content_reference', 'content_author')
