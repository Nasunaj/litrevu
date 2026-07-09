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
from django.conf import settings
from django.conf.urls.static import static
import authentification.views
import reviews.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', authentification.views.signup, name='signup'),
    path('login/', authentification.views.login_page, name='login'),
    path('logout/', authentification.views.logout_page, name='logout'),
    path('home/', authentification.views.home, name='home'),
    path('tickets/', reviews.views.ticket_list, name='ticket_list'),
    path('tickets/add/', reviews.views.ticket_create,
         name='ticket_create'),
    path('tickets/<int:ticket_id>/delete/', reviews.views.ticket_delete,
         name='ticket_delete'),
    path('tickets/<int:ticket_id>/edit/', reviews.views.ticket_update,
         name='ticket_update'),

    # review
    path('reviews', reviews.views.review_list, name='review_list'),
    path('reviews/add/', reviews.views.review_create,
         name='review_create'),
    path('reviews/<int:review_id>/delete/', reviews.views.review_delete,
         name='review_delete'),
    path('reviews/<int:review_id>/edit/', reviews.views.review_update,
         name='review_update'),

    # follow
    path('users/', reviews.views.user_list, name='user_list'),
    path('users/follow/<int:user_id>/', reviews.views.follow_user,
         name='follow_user'),
    path('users/unfollow/<int:user_id>/', reviews.views.unfollow_user,
         name='unfollow_user'),
    path('users/followed/', reviews.views.followed_users_list,
         name='followed_users_list'),
    path('users/followers/', reviews.views.followers_list,
         name='followers_list'),

    # flux
    path('feed/', reviews.views.feed, name='feed'),
    path('tickets/<int:ticket_id>/reviews', reviews.views.ticket_reviews,
         name='ticket_reviews'),

    path('tickets/add-with-review/',
         reviews.views.create_ticket_with_review,
         name='ticket_and_with_review'),

    path('users/block/<int:user_id>/', reviews.views.block_user,
         name='block_user'),
    path('users/unblock/<int:user_id>/', reviews.views.unblock_user,
         name='unblock_user'),
    path('users/blocked/', reviews.views.blocked_users_list,
         name='blocked_users_list'),

    # Redirected to /login instead of landing on http://127.0.0.1:8000/
    path('', RedirectView.as_view(url='login/')),
]

# configuration for serving developing media (image)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
