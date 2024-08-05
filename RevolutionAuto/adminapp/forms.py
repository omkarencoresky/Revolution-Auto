from django import forms
from userapp.models import UserLogin



class AdminRegisterForm(forms.ModelForm):

    class Meta:
        model = UserLogin
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password', 'role']