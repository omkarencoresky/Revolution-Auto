from django import forms
from mechanic_app.models import Mechanic

class AddMechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password', 'profile_image']
