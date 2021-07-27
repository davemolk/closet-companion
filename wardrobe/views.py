from django.shortcuts import render, redirect
from .models import Item
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="login")
def items(request):
    profile = request.user.profile
    pass


def item(request, pk):
    pass