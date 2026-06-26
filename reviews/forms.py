from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Ticket, Review


# Creating a form
class TicketForm(forms.ModelForm):
    '''
    Form for creating a new ticket.
    '''
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            # To have a larger description field
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['ticket', 'rating', 'headline', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }

    # customize the Django form's behavior
    # *args: arg1, arg2, etc.
    # **kwargs: user=request.user, data=request.POST, etc.
    # these arguments are passed to the parent constructor ->
    # ModelForm.__init__
    def __init__(self, *args, **kwargs):
        # to retrieve the 'user' value from kwargs; pop removes
        # the key and returns only the value, or None if 'user' does not exist
        user = kwargs.pop('user', None)

        # to call the parent constructor (ModelForm.__init__).
        # This allows Django --> to build the form normally
        # (loading fields, applying widgets, etc.).
        super(ReviewForm, self).__init__(*args, **kwargs)
        if user:
            # Ticket.objects.filter(user=user) returns only the tickets
            # belonging to the user
            # self.fields -> a dictionary containing all form fields
            # self.fields['ticket'] : to access the form's 'ticket' field
            # queryset -> allows filtering directly in the database
            # to avoid loading unnecessary data into RAM.
            # note: filter(), all(), and get() are selection methods
            # so they do not modify the original database.
            self.fields['ticket'].queryset = Ticket.objects.filter(user=user)
            # Bound the scores with a minimum and a maximum.
            self.fields['rating'].validators.append(MinValueValidator(1))
            self.fields['rating'].validators.append(MaxValueValidator(5))


class TicketWithReviewForm(forms.Form):
    # Ticket fields
    title = forms.CharField(max_length=128, label="Titre du billet")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label="Description du billet",
        required=False
    )
    image = forms.ImageField(
        label="Image de couverture",
        required=False
    )

    # Champs pour la critique
    rating = forms.IntegerField(
        label="Note (1-5)",
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5})
    )
    headline = forms.CharField(max_length=128, label="Titre de la critique")
    body = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label="Texte de la critique"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Retrieves the logged-in user
        super(TicketWithReviewForm, self).__init__(*args, **kwargs)

    def save(self):
        ticket = Ticket.objects.create(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            user=self.user,
            image=self.cleaned_data.get('image')
        )
        # Creation of the associated review
        review = Review.objects.create(
            ticket=ticket,
            rating=self.cleaned_data['rating'],
            headline=self.cleaned_data['headline'],
            body=self.cleaned_data['body'],
            user=self.user
        )
        return ticket, review
