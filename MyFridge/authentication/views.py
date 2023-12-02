# from django.shortcuts import render
# authentication/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import LoginForm
from .forms import RegistrationForm
from django.contrib.auth import logout
from django.shortcuts import redirect


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            # Redirect to your dashboard or recipe recommendation page
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'authentication/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'authentication/register.html', {'form': form})


def user_logout(request):
    # Call Django's logout function to log the user out
    logout(request)
    # Redirect the user to the home page or any other desired page
    return redirect('home')
