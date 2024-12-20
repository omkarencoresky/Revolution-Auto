from django import forms
from admin_app.models import UserReferral
from user_app.models import CustomUser, UserCarRecord, BookingAndQuote, SubServiceAndOption, ServicePayment

class CustomUserCreationForm(forms.ModelForm):
    """
    A form for registering a new user user.

    This form is used to collect and validate the necessary data for creating a new user.
    It includes fields for personal information and password, and handles password hashing upon saving.

    Meta:
        model (CustomUser): The model associated with this form, which is `CustomUser`.
        fields (list of str): The fields to include in the form. Excludes fields like `role` and `is_staff` 
                              which are set programmatically outside the form.

    Attributes:
        - first_name (str): The user's first name.
        - last_name (str): The user's last name.
        - email (str): The user's email address.
        - phone_no (str): The user's phone number.
        - password (str): The user's password, rendered as a password input widget.

    Widgets:
        - password: Rendered as a password input field to obscure input.
    """

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password', 'profile_image']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    
class AddCarRecord(forms.ModelForm):

    class Meta:
        model = UserCarRecord
        fields = ['car_brand', 'car_model', 'car_year', 'car_trim', 'vin_number']


class UserReferralForm(forms.ModelForm):

    class Meta:
        model = UserReferral
        fields = ["referred_email"]


class   BookingAndQuoteForm(forms.ModelForm):

    class Meta:
        model = BookingAndQuote
        fields = ["service_location", "car_brand", "car_year", "car_model", "car_trim", "car_service_type", 
                  "car_service_category"]
        
class BookingSubServiceForm(forms.ModelForm):

    class Meta:
        model = SubServiceAndOption
        fields = ['booking_id']