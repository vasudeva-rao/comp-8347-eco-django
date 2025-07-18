from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import EcoAction, EcoCategory

class EcoActionForm(forms.ModelForm):
    proof = forms.FileField(required=False, label='Proof (optional)')
    
    class Meta:
        model = EcoAction
        fields = ['title', 'description', 'category', 'points']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    ) 