from django.shortcuts import render, redirect
from .models import Item, Tag, Outfit
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ItemForm, OutfitForm
from .utils import searchItems
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse

# Create your views here.


@login_required(login_url="login")
def items(request):
    items, search_query = searchItems(request)
    tops = items.filter(type='top')
    bottoms = items.filter(type='bottom')
    dresses = items.filter(type='dress')
    shoes = items.filter(type='shoe')
    coats = items.filter(type='outerwear')
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
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ItemForm(request.POST, request.FILES)
        print('data:', request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = profile
            item.save()
            messages.success(request, 'Item successfully registered!')

            for tag in newtags:
                tag = Tag.objects.create(name=tag)
                tag.owner = profile
                tag.save()
                item.tags.add(tag)

            return redirect('items')
    
    context = {'form': form}
    return render(request, 'wardrobe/item_form.html', context)


@login_required(login_url="login")
def updateItem(request, pk):
    page = 'update'
    profile = request.user.profile
    item = profile.item_set.get(id=pk)
    tags = item.tags.all()
    form = ItemForm(instance=item)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save()
            messages.success(request, 'Item updated!')
            for tag in newtags:
                tag = Tag.objects.create(name=tag)
                tag.owner = profile
                tag.save()
                item.tags.add(tag)
            return redirect('item', pk=item.id)

    context = {'page': page, 'form': form, 'tags': tags, 'item': item}
    return render(request, 'wardrobe/item_form.html', context)


@login_required(login_url="login")
def deleteItem(request, pk):
    profile = request.user.profile
    item = profile.item_set.get(id=pk)

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted!')
        return redirect('items')
    
    context = {'object': item}
    return render(request, 'delete_template.html', context)


@login_required(login_url="login")
def deleteTag(request, pk):
    profile = request.user.profile
    tag = profile.tag_set.get(id=pk)

    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag deleted!')
        return redirect(request.GET['next'])
    
    context = {'object': tag}
    return render(request, 'delete_template.html', context)


@login_required(login_url="login")
def outfits(request):
    profile = request.user.profile
    outfits = profile.outfit_set.all()
    context = {'outfits': outfits}
    return render(request, 'wardrobe/outfits.html', context)


@login_required(login_url="login")
def outfit(request, pk):
    outfitObj = Outfit.objects.get(id=pk)
    context = {'outfit': outfitObj}
    return render(request, 'wardrobe/single_outfit.html', context)


class createOutfit(LoginRequiredMixin, CreateView):
    model = Outfit
    form_class = OutfitForm
    template_name = 'wardrobe/outfit_form.html'
    success_url = reverse_lazy('outfits')

    def form_valid(self, form):
        outfit = form.save(commit=False)
        outfit.owner = self.request.user.profile
        outfit.save()
        messages.success(self.request, 'Outfit created!')

        return super().form_valid(form)

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(createOutfit, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    
class updateOutfit(LoginRequiredMixin, UpdateView):
    model = Outfit
    form_class = OutfitForm
    template_name = 'wardrobe/outfit_form.html'

    def get_form_kwargs(self):
        kwargs = super(updateOutfit, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('outfit', kwargs={'pk': self.object.pk})

@login_required(login_url="login")
def deleteOutfit(request, pk):
    profile = request.user.profile
    outfit = profile.outfit_set.get(id=pk)

    if request.method == 'POST':
        outfit.delete()
        messages.success(request, 'Outfit deleted!')
        return redirect('outfits')

    context = {'object': outfit}
    return render(request, 'delete_template.html', context)