from django.forms import ModelForm
from .models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'type', 'image', 'sell']
        labels = {
            'name': 'Item name',
            'description': 'Item description',
            'type': 'Item type',
            'image': 'Item image', 
            'sell': 'For sale?'
        }
