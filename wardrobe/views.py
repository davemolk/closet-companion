from django.shortcuts import render, redirect
from .models import Item, Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ItemForm

# Create your views here.


#filter by user
def items(request):
    profile = request.user.profile
    items = profile.item_set.all()
    tops = Item.objects.filter(type='top')
    bottoms = Item.objects.filter(type='bottom')
    dresses = Item.objects.filter(type='dress')
    shoes = Item.objects.filter(type='shoe')
    coats = Item.objects.filter(type='coat')
    handbags = Item.objects.filter(type='handbag')
    context = {
        'tops': tops, 
        'bottoms': bottoms,
        'dresses': dresses,
        'shoes': shoes,
        'coats': coats,
        'handbags': handbags,
        'items': items,
    }

    return render(request, 'wardrobe/items.html/', context)


@login_required(login_url="login")
def item(request, pk):
    item = Item.objects.get(id=pk)
    tags = item.objects.all()
    context = {'item': item, 'tags': tags}
    return render(request, 'wardrobe/single_item.html', context)


@login_required(login_url="login")
def createItem(request):
    profile = request.user.profile
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = profile
            item.save()

        return redirect('account')
    
    context = {'form': form}
    return render(request, 'wardrobe/item_form.html', context)


@login_required(login_url="login")
def updateItem(request, pk):
    profile = request.user.profile
    item = profile.item_set.get(id=pk)
    form = ItemForm(instance=item)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect('account')

    context = {'form': form, 'item': item}
    return render(request, 'wardrobe/item_form.html', context)


@login_required(login_url="login")
def deleteItem(request, pk):
    profile = request.user.profile
    item = profile.item_set.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('account')
    
    context = {'object': item}
    return render(request, 'delete_template.html', context)
