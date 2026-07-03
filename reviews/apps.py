"""Configuration of the Django reviews application.

This module define the ReviewsConfig class, which extends AppConfig to
configure the reviews application.
"""
from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Configuration class for the reviews application.

    This class allows Django recognize and load the reviews application, which
    manages features related to tickets, reviews and users relationship.

    name (str): python name of the application.
    """

    name = 'reviews'
