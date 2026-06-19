from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)

    # Utilisateur qui a créé le ticket
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Si l'utilisateur est supprimé, ses tickets le seront aussi
        related_name='tickets' # Permet d’accéder aux tickets d’un utilisateur via user.tickets.all().
    )

    # Date de création (automatique)
    time_created = models.DateTimeField(auto_now_add=True)

    # Image de couverture
    image = models.ImageField(upload_to='tickets/', blank=True)

    # Méthode pour afficher le ticket de façon lisible dans Admin
    def __str__(self):
        return f"Ticket: {self.title} par {self.user}"

class UserFollows(models.Model):
    # Utilisateur qui suit
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )

    # Utilisateur suivi
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    # Date de création (automatique)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Eviter les doublons (un utilisateur ne peut pas suivre 2 fois la même personne)
        unique_together = ('user', 'followed_user')

class Review(models.Model):
    # Lien vers le ticket
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE,related_name='reviews')

    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])

    #titre de la critique
    headline = models.CharField(max_length=128)

    body = models.CharField(max_length=8192, blank=True)

    # Utilisateur qui a écrit la critique
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Critique de {self.user.username} pour {self.ticket.title} : {self.rating}"