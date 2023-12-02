# main/urls.py
from django.urls import path
# Import LoginView from Django's authentication views
from django.contrib.auth.views import LoginView
from .views import home, recipe_list, recipe_detail
# Adjust the import to match your view
from .views import home, CustomLoginView

urlpatterns = [
    path('', home, name='home'),
    path('authentication/login/', CustomLoginView.as_view(), name='login'),
    path('recipes/', recipe_list, name='recipes'),
    path('recipes/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    # Add other URL patterns as needed
]
