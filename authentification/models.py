"""Custom user model for the litrevu application.

This module defines the User model, which extends AbstractUser to add a role
field for distinguishing administrators from regular users.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending AbstractUser.

    ROLE_CHOICE(list) : list of available roles for a user. Each role is a
    represented as a tuple(value, label).
    role(CharField): User's role (ADMIN or USER).
    """

    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('USER', 'Utilisateur'), ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER',
    )
