from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import Ticket


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
