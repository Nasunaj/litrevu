"""Forms for managing tickets and reviews in this application.

This module defines the Django forms used to create and edit tickets and
reviews.
"""
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Ticket, Review


# Creating a form
class TicketForm(forms.ModelForm):
    """Form for creating and editing a ticket.

    This form is linked to the Ticket model and allows entering:
    a title (required), a description (optional), and a image (optional).
    """

    class Meta:
        """Configuration of the form linked Ticket model.

        Attributes:
        - model (Ticket): Django model associated with the form.
        - fields (list): List of fields to include in the form.
        - widgets (dict): Customization of widgets for specific fields.
        """

        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            # To have a larger description field
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ReviewForm(forms.ModelForm):
    """Form for creating and editing a review.

    This form is linked to the Review model and allows entering:
    a linked ticket (filter to display only user's tickets), rating (betwwen 1
    and 5, required), headline (required), body (text review, required).
    """

    class Meta:
        """Configuration of the form linked Review model."""

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
        """Initialize the form and filter the available tickets."""
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
    """Combined form to create a ticket and a review in a single step.

    This form allows entering all the necessary information to:
    - Create a new ticket (title, description, image).
    - Create an associated review (rating, headline, body).
    """

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
        """Initialize the form and stores the logged-in user."""
        self.user = kwargs.pop('user', None)  # Retrieves the logged-in user
        super(TicketWithReviewForm, self).__init__(*args, **kwargs)

    def save(self):
        """Create a ticket and an associated review in the database.

        Uses the validated form data to:
        - Create a new ticket associated with the user.
        Create a review associated with the ticket and the user.

        :return a tuple ticket (Ticket) and review (Review).
        """
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
