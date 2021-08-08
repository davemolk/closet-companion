from django.forms import ModelForm
from .models import Item, Outfit
from django import forms
from django.utils.safestring import mark_safe


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, items):
        if items.url:
            return mark_safe("<img src='%s'  style='height:125px;width:115px;'/>" % items.url)
        else:
            return mark_safe("<img src='%s' style='height:125px;width:115px;'/>" % items.imageURL)
        # return "%s" % items.imageURL

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'type', 'image', 'url', 'sell', 'price']
        labels = {
            'name': 'Item name',
            'description': 'Item description',
            'type': 'Item type',
            'image': 'Item image', 
            'url': 'Image url (if not uploading an image)',
            'sell': 'For sale?',
            'price': 'Price (if item is for sale)',
        }

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


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

