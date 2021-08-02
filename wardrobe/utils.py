from .models import Item, Tag
from django.db.models import Q

def searchItems(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    profile = request.user.profile
    items = profile.item_set.all().distinct().filter(
        Q(name__icontains=search_query) | 
        Q(description__icontains=search_query) |
        Q(type__icontains=search_query) |
        Q(tags__in=tags)
    )

    return items, search_query