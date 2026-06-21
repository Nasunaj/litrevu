from django import forms
from .models import Ticket

# Creation d'un formulaire
class TicketForm(forms.ModelForm):
    '''
    Form for creating a new ticket.
    '''
    class Meta:
        model = Ticket
        fields = ['title', 'description','image']
        widgets = {
            # Pour avoir un champs de description plus grand
            'description': forms.Textarea(attrs={'rows': 4}),
        }