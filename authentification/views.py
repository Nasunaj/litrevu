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
    logout(request)
    # Clear existing messages
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, "Déconnexion réussie !")
    return redirect('login')
