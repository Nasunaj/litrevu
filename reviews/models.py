from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class Ticket(models.Model):
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
        return f"Ticket: {self.title} par {self.user}"


class UserFollows(models.Model):
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
        # Avoid duplicates (a user cannot follow the same person twice)
        unique_together = ('user', 'followed_user')


class Review(models.Model):
    # Link to the ticket
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE,
                               related_name='reviews')

    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])

    headline = models.CharField(max_length=128)

    body = models.CharField(max_length=8192, blank=True)

    # User who wrote the review
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Critique de {self.user.username} pour {self.ticket.title} : "
                f"{self.rating}")
