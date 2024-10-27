from django.forms import ModelForm
from .models import Password
from django import forms
from django.contrib.auth.models import User

class CreatePasswordForm(ModelForm):
    sharedWith = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'shared-with-checkbox'})
    )
    
    class Meta:
        model = Password
        fields = ['name', 'url', 'password', 'passwordTag', 'shared', 'sharedWith']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control'}) 