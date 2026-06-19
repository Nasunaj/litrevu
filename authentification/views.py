from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'authentification/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie !')
            return redirect('home')
        else:
            messages.error(request,"Erreur lors de l'inscription.")
    else:
        form = UserCreationForm()
        return render(request, 'authentification/signup.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Vider les messages existants
                storage = messages.get_messages(request)
                storage.used = True  # Marque les messages comme "utilisés" (supprimés)

                messages.success(request,"Connexion réussie !")
                return redirect('home')
            else:
                messages.error(request,"Identifiants invalides.")
        else:
            messages.error(request,"Identifiants invalides.")
    else:
        form = AuthenticationForm()
        return render(request, 'authentification/login.html', {'form': form})

def logout_page(request):
    logout(request)
    # Vider les messages existants
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request,"Déconnexion réussie !")
    return redirect('login')
