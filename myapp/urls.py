"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# myapp/urls.py

from django.urls import path
from . import views
from .views import consultation_view, contact_view, information_view

urlpatterns = [
    path("register", views.register, name="register"),
    path("", views.index, name="index"),
    path("logout", views.logout, name="logout"),
    path("home", views.home, name="home"),
    path('login', views.login, name='login'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('profile/', views.profile_router, name='profile'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/view/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('contact/', contact_view, name='contact'),
    path("consultation/", consultation_view, name="consultation"),
    path('information/<int:plan_id>/<str:plan_type>/', views.information_view, name='information'),

]



# urlpatterns = [
#     # your other URLs...
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
