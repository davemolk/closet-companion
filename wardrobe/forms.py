from django.forms import ModelForm
from .models import Item
from django import forms


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'type', 'image', 'tags', 'sell']
        labels = {
            'name': 'Item name',
            'description': 'Item description',
            'type': 'Item type',
            'image': 'Item image', 
            'sell': 'For sale?'
        }
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
