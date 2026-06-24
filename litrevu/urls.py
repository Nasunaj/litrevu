"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
import authentification.views
import reviews.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',authentification.views.signup, name='signup'),
    path('login/',authentification.views.login_page, name='login'),
    path('logout/',authentification.views.logout_page, name='logout'),
    path('home/',authentification.views.home, name='home'),
    path('tickets/',reviews.views.ticket_list, name='ticket_list'),
    path('tickets/add/',reviews.views.ticket_create, name='ticket_create'),
    path('tickets/<int:ticket_id>/delete/',reviews.views.ticket_delete, name='ticket_delete'),
    path('tickets/<int:ticket_id>/edit/',reviews.views.ticket_update, name='ticket_update'),

    # review
    path('reviews',reviews.views.review_list, name='review_list'),
    path('reviews/add/',reviews.views.review_create, name='review_create'),
    path('reviews/<int:review_id>/delete/',reviews.views.review_delete, name='review_delete'),
    path('reveiws/<int:review_id>/edit/',reviews.views.review_update, name='review_update'),

    # follow
    path('users/',reviews.views.user_list, name='user_list'),
    path('users/follow/<int:user_id>/',reviews.views.follow_user,name='follow_user'),
    path('users/unfollow/<int:user_id>/',reviews.views.unfollow_user,name='unfollow_user'),
    path('users/followed/',reviews.views.followed_users_list, name='followed_users_list'),
    # path('', RedirectView.as_view(url='login/')),  # Redirige / vers /login au lieu d'arriver sur http://127.0.0.1:8000/
]
