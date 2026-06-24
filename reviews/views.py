from django.contrib import messages
from django.db.models import Q # pour les requêtes

from authentification.models import User
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user) # Uniquement les tickets de l'utilisateur
    return render(request,'reviews/ticket_list.html',{'tickets':tickets})

@login_required
def ticket_create(request):
    # Vérification que la requête est de type POST
    if request.method == 'POST':
        # request.POST : Contient toutes les données textuelles du formulaire (sous forme de dictionnaire)
        # request.FILES : Contient tous les fichiers uploadés via le formulaire (dictionnaire)
        form = TicketForm(request.POST,request.FILES) # request.FILES pr gérer les images
        if form.is_valid(): # vérification si le formulaire est valide (tous les champs sont corrects)
            ticket = form.save(commit=False) # sauvegarde le ticket sans l'enregistrer en base de données
            ticket.user = request.user # pr Associer le ticket à l'utilisateur connecté (request.user)
            ticket.save() # Enregistrement du ticket en base de données
            messages.success(request, "Ticket bien ajouté.")
            return redirect('ticket_list') # Redirige vers la liste des tickets

        else:
            messages.error(request,"Veuillez corriger les erreurs ci-dessous.")
    else:
        form = TicketForm() # création d'un formulaire vide
        #Aaffiche du template avec le formulaire
        return render(request, 'reviews/ticket_form.html', {'form': form,'action': 'Ajouter'})

@login_required
def ticket_update(request,ticket_id):
    ticket = get_object_or_404(Ticket,pk=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST,request.FILES,instance=ticket)
        if form.is_valid():
            form.save()
            messages.success("Billet modifié.")
            return redirect('ticket_list')
        else:
            messages.error(request,"Veuillez corriger les erreurs ci-dessous")
    else:
        form = TicketForm(instance=ticket)
        return render(request, 'reviews/ticket_form.html', {'form': form,'action': 'Modifier','ticket': ticket})



@login_required
def ticket_delete(request,ticket_id):
    # Pr récupère un billet ou retourner une erreur 404 s’il n’existe pas.
    ticket = get_object_or_404(Ticket, pk=ticket_id,user=request.user)
    if request.method == 'POST':
        ticket.delete()
        messages.success("Billet supprimé.")
        return redirect('ticket_list')
    return render(request, 'reviews/ticket_delete.html', {'ticket': ticket})


# ----- Reviews-------------
@login_required
def review_list(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request,'reviews/review_list.html',{'reviews':reviews})

@login_required
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST,user = request.user)
        if form.is_valid():
            # Comme il manque user on prépare la base sans sanvegarder
            review = form.save(commit=False)
            review.user = request.user # on ajouter user (celui qui connecté ici)
            review.save() # enfin on sauvegarde
            messages.success(request,"Critique ajoutée.")
            return redirect('review_list')
        else:
            messages.error("Veuillez corriger les erreurs ci-dessous")
    else:
        form = ReviewForm(user = request.user)
        return render(request, 'reviews/review_form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def review_update(request,review_id):
    review = get_object_or_404(Review,id=review_id,user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST,instance=review, user = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Critique modifiée.")
            return redirect('review_list')
        else:
            messages.error("Veuillez corriger les erreurs ci-dessous")
    else:
        form = ReviewForm(instance=review, user = request.user)
        return render(request,'reviews/review_form.html', {'form': form, 'action': 'Valider la modification','review': review})

@login_required
def review_delete(request,review_id):
    review = get_object_or_404(Review,id=review_id,user=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request,"Critique supprimée.")
        return redirect('review_list')
    return render(request, 'reviews/review_delete.html', {'review': review})


# ----------- Follow -------------

# Vue pour la liste de tous les utilisateurs en excluant soi-même
@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'reviews/user_list.html', {'users': users})

# Vue pour suivre un utilisateur
@login_required
def follow_user(request,user_id):
    user_to_follow = get_object_or_404(User,id=user_id)

    if user_to_follow == request.user:
        messages.error(request,"Il n'est pas possible de se suivre soi-même.")
        return redirect('user_list')

    if UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():
        messages.error(request,f"Vous suivez déjà {user_to_follow.username}.")
        return redirect('user_list')

    # Création du suivi
    UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
    messages.success(request,f"Vous suivez maintenant {user_to_follow.username}.")
    return redirect('user_list')

# Vue pour se désabonner d'un utilisateur
@login_required
def unfollow_user(request,user_id):
    user_to_unfollow = get_object_or_404(User,id=user_id)

    # Vérification : est ce que le suivi existe?
    follow_relationship = UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).first()
    if not follow_relationship:
        messages.error(request,f"Vous ne suivez pas {user_to_unfollow.username}.")
        return redirect('followed_users_list')

    # Suppression du suivi
    follow_relationship.delete()
    messages.success(request,f"Vous ne suivez pas {user_to_unfollow.username}.")
    return redirect('followed_users_list')

@login_required
def followed_users_list(request):
    followed_users = request.user.following.all()
    return render(request, 'reviews/followed_users_list.html', {'followed_users': followed_users})


# Vues pr flux personnalisé
@login_required
def feed(request):
    # On va récupérer l'ensemble des données nécessaires
    current_user = request.user # l'utilisateur connecté

    # les utilisateurs suivi par current_user
    followed_users = current_user.following.values_list('followed_user', flat=True)

    # les billets (ceux de current_user et ceux des utilisateurs qu'il suit)
    tickets = Ticket.objects.filter(
        Q(user = current_user) | Q(user__in=followed_users)
    ).distinct().order_by('-time_created')

    # Les critiques (de current_user et celles des utilisateurs qu'il suit et les critiques sur les billets de current_user)
    reviews = Review.objects.filter(
        Q(user = current_user) | Q(user__in=followed_users) | Q(ticket__user = current_user)
    )

    # Fusion dans une seule liste
    combined = []
    for ticket in tickets:
        me = 1 if ticket.user == current_user else 0
        combined.append({
            'type': 'ticket',
            'object': ticket,
            'time_created': ticket.time_created,
            'me':me
        })
    for review in reviews:
        me = 1 if review.user == current_user else 0
        combined.append({
            'type': 'review',
            'object': review,
            'time_created': review.time_created,
            'me':me
        })

    combined.sort(key=lambda x: x['time_created'], reverse=True)

    return render(request, 'reviews/feed.html', {'combined': combined})

@login_required
def ticket_reviews(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    reviews = Review.objects.filter(ticket=ticket).order_by('-time_created')
    return render(request, 'reviews/ticket_reviews.html', {'ticket':ticket,'reviews': reviews})