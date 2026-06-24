from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Ticket, Review


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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['ticket', 'rating','headline','body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}), # Champs + grds pr txt
        }

    # personnaliser le comportement du formulaire Django
    # *args : arg1, arg2,etc.
    # **kwargs : user=request.user, data=request.POST,etc.
    # ces arguments sont transmis au constructeur parent -> ModelForm.__init__
    def __init__(self, *args, **kwargs):
        # pr récupérer la valeur de user dans kwargs, pop permet de supprimer
        # la clé et retourne uniquement la valeur, None si user n'exsite pas.
        user = kwargs.pop('user',None)

        # pr appeler le constructeur parent (ModelForm.__init__).
        # Ce qui permet à Django --> construction normale du formulaire
        # (charger les champs, appliquer les widgets, etc.).
        super(ReviewForm, self).__init__(*args, **kwargs)
        if user:
            # Ticket.objects.filter(user=user) retourne seulement les tickets
            # de user
            # self.fields->un dictionnaire contenant tous les champs du formulaire
            # self.fields['ticket'] : pr accèder au champ ticket du formulaire
            # queryset -> permet de filtrer directement dans la base de données
            # pour éviter de charger des données inutiles en RAM.
            # remarque : filter(), all(), get() sont vu comme pour séléctionner
            # donc ne modifie pas la base originale
            self.fields['ticket'].queryset = Ticket.objects.filter(user=user)
            # Encadrer les notes avec un min et un max
            self.fields['rating'].validators.append(MinValueValidator(1))
            self.fields['rating'].validators.append(MaxValueValidator(5))