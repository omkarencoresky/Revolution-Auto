from django import forms
from .models import UserLogin

class CustomUserCreationForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    # password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = UserLogin
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password']

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password_hash'])
    #     if commit:
    #         user.save()
    #     return user