from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Memory


class SignUpForm(UserCreationForm):
    """customized form for signup """
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MemoryForm(forms.ModelForm):
    """Memory form"""
    class Meta:
        model = Memory
        fields = ('content',)
        exclude = ('user', 'created_at', 'updated_at',)

        widget = {
            'content': forms.Textarea(attrs={
                'placeholder': 'A max length is 128',
                'class': 'form-control',
            })
        }
