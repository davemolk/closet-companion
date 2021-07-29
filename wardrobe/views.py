from django.shortcuts import render, redirect
from .models import Item, Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ItemForm
from .utils import searchItems

# Create your views here.


@login_required(login_url="login")
def items(request):
    items, search_query = searchItems(request)
    tops = items.filter(type='top')
    bottoms = items.filter(type='bottom')
    dresses = items.filter(type='dress')
    shoes = items.filter(type='shoe')
    coats = items.filter(type='coat')
    handbags = items.filter(type='handbag')
    others = items.filter(type='other')
    context = {
        'tops': tops, 
        'bottoms': bottoms,
        'dresses': dresses,
        'shoes': shoes,
        'coats': coats,
        'handbags': handbags,
        'others': others,
    }

    return render(request, 'wardrobe/items.html/', context)


@login_required(login_url="login")
def item(request, pk):
    itemObj = Item.objects.get(id=pk)
    tags = itemObj.tags.all()
    context = {'item': itemObj, 'tags': tags}
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

        return redirect('items')
    
    context = {'form': form}
    return render(request, 'wardrobe/item_form.html', context)


@login_required(login_url="login")
def updateItem(request, pk):
    page = 'update'
    profile = request.user.profile
    item = profile.item_set.get(id=pk)
    form = ItemForm(instance=item)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect('items')

    context = {'page': page, 'form': form, 'item': item}
    return render(request, 'wardrobe/item_form.html', context)


@login_required(login_url="login")
def deleteItem(request, pk):
    profile = request.user.profile
    item = profile.item_set.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('items')
    
    context = {'object': item}
    return render(request, 'delete_template.html', context)
