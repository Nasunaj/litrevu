"""Admin interface configuration module for the User model.

This module customizes the display and filtering of users in the Django admin
panel for this application
"""

# To create and to personalise admin interface (/admin)
from django.contrib import admin
# Import UserAdmin class of Django to manage User model in admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """Custom class to manage the display of the User model in Django admin.

    This class extends UserAdmin to :
    - display the username, email, role and is_staff field in the table
    - Allow filtering user by role or is_staff
    """

    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')


admin.site.register(User, CustomUserAdmin)
