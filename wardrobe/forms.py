from django.forms import ModelForm
from .models import Item, Outfit
from django import forms

class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, item):
        return "%s" % item.name

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
        fields = ['name', 'description', 'item']
    
    item = CustomModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(OutfitForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(
            owner=self.request.user.profile)

    #     if kwargs.get('instance'):
    #         initial = kwargs.setdefault('initial', {})
    #         initial['item'] = [i.pk for i in kwargs['instance'].item_set.all()]

    # def save(self, commit=True):
    #     instance = forms.ModelForm.save(self, False)

    #     old_save_m2m = self.save_m2m
    #     def save_m2m():
    #         old_save_m2m()
    #         instance.item_set.clear()
    #         instance.item_set.add(*self.cleaned_data['item'])
    #     self.save_m2m = save_m2m

    #     if commit:
    #         instance.save()
    #         self.save_m2m

    #     return instance