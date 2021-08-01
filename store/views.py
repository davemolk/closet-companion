from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Order, OrderItem, ShippingAddress
from user.models import Profile
from wardrobe.models import Item
import datetime
from django.contrib.auth.decorators import login_required
from .utils import cartData, searchItems

# Create your views here.

@login_required(login_url="login")
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    items = Item.objects.filter(sell=True)
    context = {'items': items}
    return render(request, 'store/store.html', context)
    
