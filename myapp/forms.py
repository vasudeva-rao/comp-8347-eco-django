from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tip, UserUpload

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['title', 'description', 'category']

class UserUploadForm(forms.ModelForm):
    class Meta:
        model = UserUpload
        fields = ['title', 'file']

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user 