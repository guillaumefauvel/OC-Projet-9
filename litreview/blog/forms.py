from django import forms
from blog.models import Ticket

class Ticket_Creation_Form(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('content_reference', 'content_author', 'user_comment')
