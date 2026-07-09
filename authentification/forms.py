from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import ton modèle User personnalisé

class CustomUserCreationForm(UserCreationForm):
    """Custom registration form for the User model."""

    class Meta:
        #  Use your custom User model
        model = User
        # Fields to display
        fields = ('username',)