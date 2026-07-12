"""Views for the LITRevu application.

Handles ticket, review, and user follow functionalities, including:
- Creating, updating, and deleting tickets and reviews.
- Managing user follow relationships.
- Displaying personalized feeds and lists.
"""
import os
from django.contrib import messages
# from django.core.files.storage import default_storage
# For requests
from django.db.models import Q
# from urllib.parse import unquote
from authentification.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from litrevu import settings
from .forms import TicketForm, ReviewForm, TicketWithReviewForm
from .models import Ticket, Review, UserFollows, BlockedUser


@login_required
def ticket_list(request):
    """Display a list of tickets created by the current user."""
    # Only the user's tickets
    tickets = Ticket.objects.filter(user=request.user).order_by(
        '-time_created')
    # Pagination ticket
    ticket_paginator = Paginator(tickets, 5)
    ticket_page_number = request.GET.get('ticket_page')
    ticket_page_obj = ticket_paginator.get_page(ticket_page_number)
    return render(request, 'reviews/ticket_list.html',
                  {
                      # 'tickets': tickets,
                      'tickets': ticket_page_obj,
                  })


@login_required
def ticket_create(request):
    """Handle the creation of a new ticket.

    :arg request: (HttpRequest) contains form data and files for ticket
    creation

    :return redirects to ticket list on success or renders the form with
    errors.
    """
    # Verification that the request is of type POST
    if request.method == 'POST':
        # request.POST: Contains all the form's text data (as a dictionary)
        # request.FILES: Contains all files uploaded via the form (dictionary)
        # request.FILES to manage images
        form = TicketForm(request.POST, request.FILES)
        # vérification if the fom is valid (all the fiels are correct)
        if form.is_valid():
            # Save the ticket without saving in the database.
            ticket = form.save(commit=False)
            # To associate the ticket with the logged-in user (request.user)
            ticket.user = request.user
            ticket.save()  # Saving the ticket
            messages.success(request, "Ticket bien ajouté.")
            return redirect('ticket_list')

        else:
            messages.error(request,
                           "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = TicketForm()  # création d'un formulaire vide
        # Display the template containing the form.
        return render(request, 'reviews/ticket_form.html',
                      {'form': form, 'action': 'Ajouter'})


@login_required
def ticket_update(request, ticket_id):
    """Handle the update of a ticket (and image managing).

    :arg:
    - request: (HttpRequest) contains updated form data and files.
    - ticket_id: (int) id of the ticket to update.

    :return HttpResponse: redirects to ticket list on success or renders the
    form with errors.
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    # old path
    old_image_path = None
    if ticket.image:
        old_image_path = os.path.join(settings.MEDIA_ROOT, ticket.image.name)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            # If a new image is uploaded or if "Clear" is checked
            print("Ok je suis")
            if 'image' in request.FILES or 'image-clear' in request.POST:
                if old_image_path and os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                        print(f"old image removed : {old_image_path}")
                    except Exception as e:
                        print(f"Error removing : {e}")
                else:
                    print(f"Old image not found : {old_image_path}")

                if 'image-clear' in request.POST:
                    ticket.image = None
            form.save()
            messages.success(request,
                             "Billet modifié.")
            return redirect('ticket_list')
        else:
            messages.error(request,
                           "Veuillez corriger les erreurs ci-dessous")
    else:
        form = TicketForm(instance=ticket)
        return render(request, 'reviews/ticket_form.html',
                      {'form': form, 'action': 'Modifier',
                       'ticket': ticket})

# @login_required
# def ticket_update(request, ticket_id):
#     ticket = get_object_or_404(Ticket, pk=ticket_id)
#     if request.method == 'POST':
#         form = TicketForm(request.POST, request.FILES, instance=ticket)
#         if form.is_valid():
#             # If a new image is uploaded or if "Clear" is checked
#             print("Ok je suis")
#             if 'image' in request.FILES or 'image-clear' in request.POST:
#                 print("image quelque part")
#                 if ticket.image:
#                     print(f"ticket.image : {ticket.image}")
#                     # Construct the CORRECT path:
#                     # MEDIA_ROOT + 'tickets/' + filename
#                     image_path = os.path.join(settings.MEDIA_ROOT, 'tickets',
#                                               ticket.image.name)
#                     print(f"Chemin du fichier à supprimer : {image_path}")
#                     print(f"Fichier existe ? : {os.path.exists(image_path)}")
#
#                     if os.path.exists(image_path):
#                         try:
#                             os.remove(image_path)
#                             print(f"✅ Fichier supprimé : {image_path}")
#                         except Exception as e:
#                             print(f"❌ Erreur lors de la suppression : {e}")
#                     else:
#                         print(f"❌ Fichier introuvable : {image_path}")
#
#                     # If "Clear" is checked, the field is deleted.
#                     if 'image-clear' in request.POST:
#                         ticket.image = None
#             form.save()
#             messages.success(request,
#                              "Billet modifié.")
#             return redirect('ticket_list')
#         else:
#             messages.error(request,
#                            "Veuillez corriger les erreurs ci-dessous")
#     else:
#         form = TicketForm(instance=ticket)
#         return render(request, 'reviews/ticket_form.html',
#                       {'form': form, 'action': 'Modifier',
#                        'ticket': ticket})


@login_required
def ticket_delete(request, ticket_id):
    """Handle the deletion of a ticket (and image).

    :arg:
    - request: (HttpRequest) confirms deletion via POST.
    - ticket_id: (int) id of the ticket to delete.

    :return HttpResponse: redirects to ticket list on success or renders
    confirmation page.
    """
    # To retrieve a ticket or return a 404 error if it does not exist.
    ticket = get_object_or_404(Ticket, pk=ticket_id, user=request.user)
    old_image_path = None
    if ticket.image:
        old_image_path = os.path.join(settings.MEDIA_ROOT, ticket.image.name)
    if request.method == 'POST':
        # delete image too in the media/tickets/
        if old_image_path and os.path.exists(old_image_path):
            try:
                os.remove(old_image_path)
                print(f"old image removed : {old_image_path}")
            except Exception as e:
                print(f"Error removing : {e}")
        else:
            print(f"Old image not found : {old_image_path}")

        ticket.delete()

        messages.success(request, "Billet supprimé.")
        return redirect('ticket_list')
    return render(request, 'reviews/ticket_delete.html',
                  {'ticket': ticket})


# ----- Reviews-------------
@login_required
def review_list(request):
    """Display a list of reviews created by the current user."""
    reviews = Review.objects.filter(user=request.user).order_by(
        '-time_created')
    # Pagination review
    review_paginator = Paginator(reviews, 5)
    review_page_number = request.GET.get('review_page')
    review_page_obj = review_paginator.get_page(review_page_number)
    return render(request, 'reviews/review_list.html',
                  {
                      # 'reviews': reviews,
                      'reviews': review_page_obj,
                  })


@login_required
def review_create(request):
    """Handle the creation of a new review.

    :arg request : (HttpRequest) contains form data for review creation.

    :return HttpResponse: Redirects to review list on success or renders the
    form with errors.
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES,
                          user=request.user)
        if form.is_valid():
            # The user is missing
            # so first we prepare the database without saving.
            review = form.save(commit=False)
            review.user = request.user  # we add user
            review.save()  # end we save
            messages.success(request, "Critique ajoutée.")
            return redirect('review_list')
        else:
            messages.error("Veuillez corriger les erreurs ci-dessous")
    else:
        form = ReviewForm(user=request.user)
        return render(request, 'reviews/review_form.html',
                      {'form': form, 'action': 'Ajouter'})


@login_required
def review_update(request, review_id):
    """Handle the update of an existing review.

    :arg:
    - request : (HttpRequest) contains updated form data.
    - review_id : (int) id of the review to update.

    :return HttpResponse: Redirects to review list on success or renders the
    form with errors.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review,
                          user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Critique modifiée.")
            return redirect('review_list')
        else:
            messages.error("Veuillez corriger les erreurs ci-dessous")
    else:
        form = ReviewForm(instance=review, user=request.user)
        return render(request, 'reviews/review_form.html',
                      {'form': form,
                       'action': 'Valider la modification', 'review': review})


@login_required
def review_delete(request, review_id):
    """Handle the deletion of a review.

    :arg:
    - request: (HttpRequest) confirms deletion via POST.
    - review_id : (int) id of the review to delete.

    :return HttpResponse: redirects to review list on success or renders
    confirmation page.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Critique supprimée.")
        return redirect('review_list')
    return render(request, 'reviews/review_delete.html',
                  {'review': review})


# ----------- Follow -------------
# View for the list of all users, excluding oneself
# @login_required
# def user_list(request):
#     """Display a list of all users, excluding the current user."""
#     users = User.objects.exclude(id=request.user.id)
#     return render(request, 'reviews/user_list.html',
#                   {'users': users})
@login_required
def user_list(request):
    """Display a list of users.

    :arg request: (HttpRequest) The HTTP request object.

    :return HttpResponse: Rendered template 'reviews/user_list.html
    """
    # Retrieves the requested username from the GET request.
    search_name_user = request.GET.get('search', '').strip()

    # Exclude the logged-in user from the list
    users = User.objects.exclude(id=request.user.id)

    if search_name_user:
        # Filter users whose username contains the search
        # term(case-insensitive)
        users = users.filter(username__icontains=search_name_user)

        # if no user matches
        if not users.exists():
            messages.error(request, f"Aucun utilisateur trouvé avec "
                                    f"le nom {search_name_user}.")
    # Pagination : 5 users by page
    paginator = Paginator(users, 5)  # Display 5 users by page
    # Retrieves the page number from the URL
    page_number = request.GET.get('page')
    # Retrieve the users for this page
    page_obj = paginator.get_page(page_number)
    return render(request, 'reviews/user_list.html', {
        'users': users,
        'search_name_user': search_name_user,
        'page_obj': page_obj,
    })


# View to follow a user
@login_required
def follow_user(request, user_id):
    """Handle following a user.

    :arg
    - request: (HttpRequest) initiates the follow action.
    - user_id: (int) id of the user to follow.

    :return HttpResponse: redirects to user list with success/error message.
    """
    user_to_follow = get_object_or_404(User, id=user_id)

    if user_to_follow == request.user:
        messages.error(request,
                       "Il n'est pas possible de se suivre soi-même.")
        return redirect('user_list')

    if UserFollows.objects.filter(user=request.user,
                                  followed_user=user_to_follow).exists():
        messages.error(request,
                       f"Vous suivez déjà {user_to_follow.username}.")
        return redirect('user_list')

    # Creation follow
    UserFollows.objects.create(user=request.user,
                               followed_user=user_to_follow)
    messages.success(request,
                     f"Vous suivez maintenant {user_to_follow.username}.")
    return redirect('user_list')


# View for unsubscribing from a user
@login_required
def unfollow_user(request, user_id):
    """Handle unfollowing a user.

    :arg:
        request: (HttpRequest) initiates the unfollow action.
        user_id: (int) id of the user to unfollow.

    :return HttpResponse: redirects to followed users list with success/error
    message.
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)

    # Verification: Does the tracking exist?
    follow_relationship = (UserFollows.objects.filter
                           (user=request.user,
                            followed_user=user_to_unfollow).first())
    if not follow_relationship:
        messages.error(request,
                       f"Vous ne suivez pas "
                       f"{user_to_unfollow.username}.")
        return redirect('followed_users_list')

    # Delete the follow
    follow_relationship.delete()
    messages.success(request,
                     f"Vous ne suivez pas "
                     f"{user_to_unfollow.username}.")
    return redirect('followed_users_list')


@login_required
def followed_users_list(request):
    """Display a list of users followed by the current user."""
    followed_users = request.user.following.all()
    return render(request, 'reviews/followed_users_list.html',
                  {'followed_users': followed_users})


# personnalisation feed
@login_required
def feed(request):
    """Display a personalized feed of tickets and reviews.

    Combines tickets and reviews from the current user and users they follow,
    sorted by creation date (newest first).

    :return HttpResponse: renders the feed template with combined and sorted
    content.
    """
    # We will gather all the necessary data.
    current_user = request.user  # connected user

    # Users followed by current_user
    followed_users = current_user.following.values_list('followed_user',
                                                        flat=True)

    # Tickets (current_user et users followed bu current_user)
    tickets = Ticket.objects.filter(
        Q(user=current_user) | Q(user__in=followed_users)
    ).distinct().order_by('-time_created')

    # Reviews (from the current user, from users they follow,
    # and reviews of the current user's posts)
    reviews = Review.objects.filter(
        Q(user=current_user) | Q(user__in=followed_users) |
        Q(ticket__user=current_user)
    ).order_by('-time_created')

    # # Merge into a single list
    # combined = []
    # for ticket in tickets:
    #     me = 1 if ticket.user == current_user else 0
    #     combined.append({
    #         'type': 'ticket',
    #         'object': ticket,
    #         'time_created': ticket.time_created,
    #         'me': me
    #     })
    # for review in reviews:
    #     me = 1 if review.user == current_user else 0
    #     combined.append({
    #         'type': 'review',
    #         'object': review,
    #         'time_created': review.time_created,
    #         'me': me
    #     })
    #
    # combined.sort(key=lambda x: x['time_created'], reverse=True)

    # Pagination ticket
    ticket_paginator = Paginator(tickets, 5)
    ticket_page_number = request.GET.get('ticket_page')
    ticket_page_obj = ticket_paginator.get_page(ticket_page_number)

    # Pagination review
    review_paginator = Paginator(reviews, 5)
    review_page_number = request.GET.get('review_page')
    review_page_obj = review_paginator.get_page(review_page_number)

    return render(request, 'reviews/feed.html',
                  {
                      # 'combined': combined,
                      'ticket_page_obj': ticket_page_obj,
                      'review_page_obj': review_page_obj,
                      'current_user': current_user,
                   })


@login_required
def ticket_reviews(request, ticket_id):
    """Display all reviews for a specific ticket.

    :arg:
        request : (HttpRequest) request to view ticket reviews.
        ticket_id : (int) id of the ticket to fetch reviews for.

    :return HttpResponse: renders the ticket reviews template with ticket and
    reviews.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    reviews = Review.objects.filter(ticket=ticket).order_by('-time_created')
    # Pagination review
    review_paginator = Paginator(reviews, 5)
    review_page_number = request.GET.get('review_page')
    review_page_obj = review_paginator.get_page(review_page_number)
    return render(request, 'reviews/ticket_reviews.html',
                  {
                      'ticket': ticket,
                      # 'reviews': reviews,
                      'reviews': review_page_obj,
                  })


@login_required
def create_ticket_with_review(request):
    """Handle the creation of a ticket and its associated review in one step.

    :arg request : (HttpRequest) contains form data for both ticket and review.

    :return HttpResponse: redirects to feed on success, or renders the form
    with errors.
    """
    if request.method == 'POST':
        form = TicketWithReviewForm(request.POST, request.FILES,
                                    user=request.user)
        if form.is_valid():
            ticket, review = form.save()
            messages.success(request,
                             "Billet et critique créés avec succès !")
            return redirect('feed')
    else:
        form = TicketWithReviewForm(user=request.user)
    return render(request, 'reviews/ticket_with_review_form.html',
                  {'form': form})


@login_required
def block_user(request, user_id):
    """Block a user."""
    user_to_block = get_object_or_404(User, id=user_id)

    # Verify that the user doesn't lock themselves out.
    if user_to_block == request.user:
        messages.error(request,
                       "Vous ne pouvez pas vous bloquer vous-même.")
        return redirect('user_list')

        # Verify if user is already blocked
    if BlockedUser.objects.filter(user=request.user,
                                  blocked_user=user_to_block).exists():
        messages.error(request,
                       f"Vous avez déjà bloqué "
                       f"{user_to_block.username}.")
        return redirect('user_list')

    # Create then block
    BlockedUser.objects.create(user=request.user, blocked_user=user_to_block)

    # Automatically unfollow if the user was followed
    follow_relationship = UserFollows.objects.filter(
        user=request.user, followed_user=user_to_block).first()
    if follow_relationship:
        follow_relationship.delete()
        messages.info(request, f"Vous avez été désabonné de "
                               f"{user_to_block.username}.")

    messages.success(request,
                     f"Vous avez bloqué {user_to_block.username}.")
    return redirect('user_list')


@login_required
def unblock_user(request, user_id):
    """Unblock a user."""
    user_to_unblock = get_object_or_404(User, id=user_id)

    # Verify that the block exists
    block_relationship = BlockedUser.objects.filter(
        user=request.user, blocked_user=user_to_unblock).first()
    if not block_relationship:
        messages.error(request,
                       f"Vous n'avez pas bloqué {user_to_unblock.username}.")
        return redirect('blocked_users_list')

    # Unblock user
    block_relationship.delete()
    messages.success(request,
                     f"Vous avez débloqué {user_to_unblock.username}.")
    return redirect('blocked_users_list')


@login_required
def blocked_users_list(request):
    """List all blocked users."""
    # Retrieves blocked users directly (not BlockedUser objects)
    blocked_users = BlockedUser.objects.filter(
        user=request.user
        # Returns a list of user IDs
    ).values_list('blocked_user', flat=True)

    # Converts IDs into User objects.
    blocked_users = User.objects.filter(id__in=blocked_users)

    return render(request, 'reviews/blocked_users_list.html',
                  {'blocked_users': blocked_users})


@login_required
def followers_list(request):
    """Display a list of users who follow the current user."""
    # Retrieves the users who follow the logged-in user
    # Thanks to related_name='followed_by' in UserFollows
    followers = request.user.followed_by.all()
    return render(request, 'reviews/followers_list.html',
                  {'followers': followers})
