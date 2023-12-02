# Create your views here.
# main/views.py
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.http import HttpResponse


class CustomLoginView(LoginView):
    # Add any customization if needed
    template_name = 'login.html'


def home(request):
    return render(request, 'main/home.html')  # Update the template name here


def recipe_list(request):
    # Your recipe list logic goes here
    return HttpResponse("Recipe List Page")


def recipe_detail(request, recipe_id):
    # Your recipe detail logic goes here
    return HttpResponse(f"Recipe Detail Page for Recipe ID {recipe_id}")
