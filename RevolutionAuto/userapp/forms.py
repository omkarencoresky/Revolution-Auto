from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password']

 