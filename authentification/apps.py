"""Configuration of the Django authentification application.

This module define the AuthenticationConfig class, which extends AppConfig to
configure the authentification application (models, name, dependencies,etc.)
"""
from django.apps import AppConfig


class AuthentificationConfig(AppConfig):
    """Configuration class for the authentification application.

    name (str): python name of the application.
    """

    name = 'authentification'
