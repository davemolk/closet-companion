from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile,

# Create your views here.

def index(request):
    return render(request, 'index.html')

def loginUser(request):
    pass


def signupUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            #messages.success(request, 'User account created!')
            login(request, user)
            return redirect('account')
        else:
            #messages.error(request, 'An error has occurred during registration')
            return redirect('signup')
    context = {'form': form}
    return render(request, 'user/signup.html', context)
