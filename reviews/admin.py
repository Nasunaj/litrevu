"""Admin interface configuration for reviews app.

This module save Ticket, Review and Userfollows modules in admin django
interface, allowing to manage in /admin/
"""

from django.contrib import admin
from .models import Ticket, Review, UserFollows

# Enregistrer les modèles pour qu'ils apparaissent dans Admin
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
