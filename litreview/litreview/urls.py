"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)

import authentication.views
from blog import views


urlpatterns = [

    # BASE

    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),

    # AUTHENTICATION

    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'),
    path('signup/', authentication.views.signup_page, name='signup'),

    # OTHER

    path('ticket/creation', views.create_ticket, name='ticket-creation'),
    path('ticket/list', views.ticket_list_view, name='ticket-list'),
    path('ticket/<int:ticket_id>', views.review_from_ticket, name='ticket-page'),

    path('review/creation', views.create_review, name='review-creation'),
    path('review/list', views.review_list_view, name='review-list'),

    path('userlist/', views.user_list, name='user-list'),
    path('profile/', views.profile, name='profile'),

    path('user/<int:user_id>', views.user_page, name='user-page'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
