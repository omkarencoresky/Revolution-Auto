from django import forms
from userapp.models import CustomUser
from adminapp.models import CarBrand, CarYear



class AdminRegisterForm(forms.ModelForm):
    """
    A form for registering a new admin user.

    This form is used to collect and validate the necessary data for creating a new admin user.
    It includes fields for personal information and password, and handles password hashing upon saving.

    Meta:
        model (CustomUser): The model associated with this form, which is `CustomUser`.
        fields (list of str): The fields to include in the form. Excludes fields like `role` and `is_staff` 
                              which are set programmatically outside the form.

    Attributes:
        - first_name (str): The admin user's first name.
        - last_name (str): The admin user's last name.
        - email (str): The admin user's email address.
        - phone_no (str): The admin user's phone number.
        - password (str): The admin user's password, rendered as a password input widget.

    Widgets:
        - password: Rendered as a password input field to obscure input.
    """

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password']


class Addbrandform(forms.ModelForm):

    class Meta:
        model =  CarBrand
        fields = ['brand', 'description']



class Addyearform(forms.ModelForm):

    class Meta:
        model =  CarYear
        fields = ['car_id', 'year',]
