from django.forms import ModelForm
from .models import Item
from django import forms


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'type', 'image', 'tags', 'sell']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
