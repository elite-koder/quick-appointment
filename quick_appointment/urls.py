"""
URL configuration for quick_appointment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from users.views import login_view, logout_view
from appointments.views import book_appointment, manage_appointment
from slots.views import create_slot, manage_slot

urlpatterns = [
    path('', book_appointment, name="home_view"),
    path('appointments/create', book_appointment, name="book_appointment_view"),
    path('appointments/manage', manage_appointment, name="manage_appointment_view"),
    path('slots/create', create_slot, name="create_slot_view"),
    path('slots/manage', manage_slot, name="manage_slot_view"),
    path('login', login_view, name="login_view"),
    path("logout", logout_view, name="logout_view")
]
