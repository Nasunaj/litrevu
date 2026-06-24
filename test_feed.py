import os
import django

# 1. Configure Django pour utiliser ton projet
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'litrevu.settings')
django.setup()

# 2. Importations après la configuration de Django
from authentification.models import User
from reviews.models import Ticket, Review, UserFollows
from django.db.models import Q
from django.test import RequestFactory

# 3. Fonction à tester (copiée depuis views.py)
def test_feed(current_user):
    # Les utilisateurs suivis par current_user
    followed_users = current_user.following.values_list('followed_user', flat=True)
    # print("\n--- Utilisateurs suivis par", current_user.username, "---")
    # print("followed_users (IDs) :", list(followed_users))
    # print("followed_users (noms) :", [User.objects.get(id=uid).username for uid in followed_users])

    # Les billets (ceux de current_user et ceux des utilisateurs qu'il suit)
    tickets = Ticket.objects.filter(
        Q(user=current_user) | Q(user__in=followed_users)
    ).distinct().order_by('-time_created')
    # print("\n--- Billets dans le flux ---")
    # for ticket in tickets:
    #     print(f"- {ticket.title} (par {ticket.user.username}, créé le {ticket.time_created})")

    # Les critiques (de current_user, des utilisateurs suivis, et sur les billets de current_user)
    reviews = Review.objects.filter(
        Q(user=current_user) |
        Q(user__in=followed_users) |
        Q(ticket__user=current_user)
    ).distinct().order_by('-time_created')
    # print("\n--- Critiques dans le flux ---")
    # for review in reviews:
    #     print(f"- {review.headline} (par {review.user.username}, note: {review.rating}/5, pour le billet: {review.ticket.title}, créé le {review.time_created})")

    # Fusion dans une seule liste
    combined = []
    for ticket in tickets:
        combined.append({
            'type': 'ticket',
            'object': ticket,
            'time_created': ticket.time_created
        })
    for review in reviews:
        combined.append({
            'type': 'review',
            'object': review,
            'time_created': review.time_created
        })
    combined.sort(key=lambda x: x['time_created'], reverse=True)

    # print("\n--- Liste fusionnée et triée ---")
    # for item in combined:
    #     if item['type'] == 'ticket':
    #         print(f"[BILLET] {item['object'].title} (par {item['object'].user.username}, {item['time_created']})")
    #     else:
    #         print(f"[CRITIQUE] {item['object'].headline} (par {item['object'].user.username}, note: {item['object'].rating}/5, {item['time_created']})")

    return combined

# 4. Création de données de test
def create_test_data():
    # print("\n--- Création des données de test ---")

    # Supprimer les données existantes (optionnel)
    User.objects.filter(username__in=['alice', 'bob', 'charlie']).delete()

    # Créer des utilisateurs
    alice = User.objects.create_user(username='alice', password='Alice123!', email='alice@example.com')
    bob = User.objects.create_user(username='bob', password='Bob123!', email='bob@example.com')
    charlie = User.objects.create_user(username='charlie', password='Charlie123!', email='charlie@example.com')
    #print("Utilisateurs créés : Alice, Bob, Charlie")

    # Créer des billets
    ticket1 = Ticket.objects.create(title="1984 de George Orwell", description="Un classique de la dystopie.", user=alice)
    ticket2 = Ticket.objects.create(title="Dune de Frank Herbert", description="Un chef-d'œuvre de science-fiction.", user=bob)
    ticket3 = Ticket.objects.create(title="Le Petit Prince", description="Un livre poétique.", user=charlie)
    #print("Billets créés : 1984, Dune, Le Petit Prince")

    # Créer des critiques
    review1 = Review.objects.create(ticket=ticket1, rating=5, headline="Un chef-d'œuvre !", body="Ce livre est incroyable.", user=alice)
    review2 = Review.objects.create(ticket=ticket2, rating=4, headline="Très bon", body="J'ai adoré.", user=bob)
    review3 = Review.objects.create(ticket=ticket3, rating=3, headline="Sympa", body="Un livre agréable.", user=charlie)
    review4 = Review.objects.create(ticket=ticket1, rating=5, headline="Génial", body="À lire absolument !", user=bob)  # Bob critique le billet d'Alice
    #print("Critiques créées : 4 critiques")

    # Créer des relations de suivi
    UserFollows.objects.create(user=alice, followed_user=bob)  # Alice suit Bob
    UserFollows.objects.create(user=alice, followed_user=charlie)  # Alice suit Charlie
    #print("Relations de suivi créées : Alice suit Bob et Charlie")

    return alice, bob, charlie

# 5. Exécution du test
if __name__ == "__main__":
    # Créer des données de test
    alice, bob, charlie = create_test_data()


    # Tester le flux pour Alice
    #print("\n\n=== TEST DU FLUX POUR ALICE ===")
    print(test_feed(alice))
