"""Forms for the authentication application.

This module contains custom forms for user registration and authentication.
"""

from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import ton modèle User personnalisé


class CustomUserCreationForm(UserCreationForm):
    """Custom registration form for the User model."""

    class Meta:
        """Configuration for the CustomUserCreationForm.

        Attributes:
            model (User): The custom User model to use for the form.
            fields (tuple): Fields to include in the form
            (here, only 'username').
        """

        #  Use your custom User model
        model = User
        # Fields to display
        fields = ('username',)
