"""Models for the LITRevu application.

Defines Ticket, UserFollows, and Review models for managing user interactions.
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class Ticket(models.Model):
    """Model representing a ticket in the application.

    A ticket is created by a user to request reviews for a book or article.
    It includes a title, description, optional image, and creation
    timestamp.

    Attributes:
        - title (CharField): title of the ticket.
         - description (TextField): description of the ticket (optional).
         - user (ForeignKey): user who created the ticket. Cascades on user
         deletion.
         - time_created (DateTimeField): automatic creation timestamp.
         - image (ImageField): cover image for the ticket (optional).
    """

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)

    # User who created the ticket.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # if user is deleted -> theirs tickets will delete as well too
        on_delete=models.CASCADE,
        # Provides access to a user's tickets via user.tickets.all().
        related_name='tickets'
    )

    # Creation date(automatique)
    time_created = models.DateTimeField(auto_now_add=True)

    # Image
    image = models.ImageField(upload_to='tickets/', null=True, blank=True)

    # Method to display the ticket in a readable format in Admin
    def __str__(self):
        """Return a readable representation of the ticket.

        Returns:
            str: string with ticket title and creator.
        """
        return f"Ticket: {self.title} par {self.user}"


class UserFollows(models.Model):
    """Model representing a user-follow relationship in the application.

    Tracks which users follow other users, with a creation timestamp.
    Ensures a user cannot follow the same person twice.

    Attributes:
        - user (ForeignKey): user who is following someone.
        - followed_user (ForeignKey): user who is being followed.
        - time_created (DateTimeField): automatic creation timestamp.
    """

    # User who follows
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )

    # Followed user
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    # Creation date
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the UserFollows model.

        Attributes:
            unique_together (tuple): ensures no duplicate follow relationships.
        """

        # Avoid duplicates (a user cannot follow the same person twice)
        unique_together = ('user', 'followed_user')


class Review(models.Model):
    """Model representing a review of a ticket in the pplication.

    A review is linked to a ticket and includes a rating, headline, and body.
    It is created by a user and associated with a specific ticket.

    Attributes:
        - ticket (ForeignKey): ticket being reviewed. Cascades on ticket
        deletion.
        - rating (PositiveSmallIntegerField): rating between 1 and 5.
        - headline (CharField): title of the review.
        - body (CharField): body text of the review (optional).
        - user (ForeignKey): user who wrote the review. Cascades on user
        deletion.
        - time_created (DateTimeField): automatic creation timestamp.
    """

    # Link to the ticket
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE,
                               related_name='reviews')

    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    headline = models.CharField(max_length=128)

    body = models.CharField(max_length=8192, blank=True)

    # User who wrote the review
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable representation of the review.

        Returns:
            str: string with reviewer, ticket title, and rating.
        """
        return (f"Critique de {self.user.username} pour {self.ticket.title} : "
                f"{self.rating}")
