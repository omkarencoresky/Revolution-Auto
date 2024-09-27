from django import forms
from user_app.models import CustomUser

class AddMechanicForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password', 'profile_image']
