from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # A voir plus tard les rôles à définir si nécessaire ex : crétateur / lecteurs?
    # pass
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('USER', 'Utilisateur'), ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER',
    )



