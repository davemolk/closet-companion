import json
from .models import *
from user.models import Profile
from wardrobe.models import Item, Tag
from django.shortcuts import render, redirect
from django.db.models import Q

def searchItems(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    
    items = Item.objects.filter(sell=True).distinct().filter(
        Q(name__icontains=search_query) | 
        Q(description__icontains=search_query) |
        Q(type__icontains=search_query) |
        Q(owner__username__icontains=search_query) |
        Q(tags__in=tags)
    )

    return items, search_query


def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.profile
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		orderItems = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		return redirect('login')

	return {'cartItems': cartItems ,'order': order, 'orderItems': orderItems}
