from .models import Message
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe

# from django.utils.translation import gettext_lazy as _

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Password confirmation'
        self.fields['password1'].help_text = mark_safe("Choose a password not used before or elsewhere. <br /> 8 characters minimum with no spaces. <br /> Includes letters and at least 1 number.")
        self.fields['password2'].help_text = 'Re-enter your password for verification.'