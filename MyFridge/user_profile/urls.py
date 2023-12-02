# profile/urls.py
from django.urls import path
from .views import profile_view

urlpatterns = [
    path('user_profile/', profile_view, name='profile'),
    # Add more URLs for the profile app as needed
]
