"""Views for the authentification application."""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reviews.models import Ticket, Review, UserFollows


# @login_required(login_url='login') not necessary because we defined
# in settings.py LOGIN_URL = 'login'
@login_required
def home(request):
    """Display the personalized home page for the logged-in user.

    This view retrieves and displays the user's statistics:
    - Number of tickets created.
    - Number of reviews published.
    - Number of users followed.

    :arg request: (HttpRequest) Object containing the http request data.

    :return: (HttpResponse) Rendered HTML page using the template
    authentification/home.html with the user's statistics in the context.
    """
    user = request.user
    tickets_count = Ticket.objects.filter(user=user).count()
    reviews_count = Review.objects.filter(user=user).count()
    # Nb users followed
    followed_users_count = UserFollows.objects.filter(user=user).count()
    return render(request, 'authentification/home.html', {
        'tickets_count': tickets_count,
        'reviews_count': reviews_count,
        'followed_users_count': followed_users_count,
    }
                  )


def signup(request):
    """Handle the registration of a new user.

    This view processes POST requests to create a user account. If the form is
    valid, the user is created, automatically logged-in and redirected to the
    home page. If else error, message is displayed.

    :arg request: (HttpRequest) Object containing the http request data
    :return: (HttpResponse)
    - Redirected to the home page if registration is succeeds.
    - Rendered HTML page using the template.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie !')
            return redirect('home')
        else:
            messages.error(request, "Erreur lors de l'inscription.")
    else:
        form = UserCreationForm()
        return render(request, 'authentification/signup.html',
                      {'form': form})


def login_page(request):
    """Handle the login of a user.

    This view processes POST requests to authenticate a user. If the
    identifants are valid, the user is logged in and redirected to the URL
    specified by the next parameter (or to the 'home' page by default).
    In case of an error, a message is displayed, and the form is redisplayed.

    :arg request: (HttpRequest) Object containing the http request data

    :return: (HttpResponse)
    - Redirected to the URL specified by next to or to hone if loggin succeeds.
    - Rendered the template authentification/login.html with the form.
    """
    # To retrieve the redirect URL; otherwise, it defaults to 'home'
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Clear existing messages
                storage = messages.get_messages(request)
                # Mark messages as "used" (deleted)
                storage.used = True

                messages.success(request, "Connexion réussie !")
                # return redirect('home')
                return redirect(next_url)
            else:
                messages.error(request, "Identifiants invalides.")
        else:
            messages.error(request, "Identifiants invalides.")
            return render(request, 'authentification/login.html',
                          {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'authentification/login.html',
                      {'form': form})


def logout_page(request):
    """Handle the user logout.

    This view log out the current user, removes existing flash messages to
    avoid duplicates, display a confirmation message, and then redirects to the
    login page.

    :arg request: (HttpRequest) Object containing the http request data

    :return: (HttpResponse) Redirected to the login page.
    """
    logout(request)
    # Clear existing messages
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, "Déconnexion réussie !")
    return redirect('login')
