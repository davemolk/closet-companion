from django.forms import ModelForm
from .models import Item, Outfit
from django import forms

class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, items):
        return "%s" % items.name

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'type', 'image', 'sell']
        labels = {
            'name': 'Item name',
            'description': 'Item description',
            'type': 'Item type',
            'image': 'Item image', 
            'sell': 'For sale?',
            'price': '(if item is for sale)',
        }

class OutfitForm(ModelForm):
    class Meta:
        model = Outfit
        fields = ['name', 'description', 'items']
    
    items = CustomModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(OutfitForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = Item.objects.filter(
            owner=self.request.user.profile)

