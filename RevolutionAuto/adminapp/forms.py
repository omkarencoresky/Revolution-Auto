from django import forms
from userapp.models import CustomUser
from django_ckeditor_5.widgets import CKEditor5Widget
from adminapp.models import CarBrand, CarYear, CarModel, CarTrim, Location, ServiceType, ServiceCategory, Services, SubServices



class AdminRegisterForm(forms.ModelForm):
    """
    A form for registering a new admin user.

    This form is used to collect and validate the necessary data for creating a new admin user.
    It includes fields for personal information and password, and handles password hashing upon saving.

    Attributes:
        - first_name (str): The admin user's first name.
        - last_name (str): The admin user's last name.
        - email (str): The admin user's email address.
        - phone_no (str): The admin user's phone number.
        - password (str): The admin user's password, rendered as a password input widget.
    """

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password']


class AddBrandForm(forms.ModelForm):
    """
    A form for for adding or updating car brand.

    This form is used to collect and validate the necessary data for creating a new brand.
    It includes fields for brand information and description.

    Attributes:
        - brand (str): The name of the car-brand.
        - description: extradetails or specification of the car-brand.
    """

    class Meta:
        model =  CarBrand
        fields = ['brand', 'description']


class AddYearForm(forms.ModelForm):
    """
    A form for adding or updating car years.

    This form is tied to the CarYear model and includes fields for selecting a car (car_id) and specifying the year. 
    It is intended to be used in views where users can input new car years or update existing ones. 
    The form handles validation for these fields according to the constraints defined in the CarYear model.

    Attributes:
        car_id (ModelChoiceField): A field for selecting a car instance from the database. 
        This field is automatically populated with choices representing all available cars.
        year (IntegerField): A field for specifying the year of the car. This field validates that the input is an integer.
    """

    class Meta:
        model =  CarYear
        fields = ['car_id', 'year',]


class AddModelForm(forms.ModelForm):
    """
    A form for adding or updating car models.

    This form is designed to work with the CarModel model, allowing users to specify details about a car model, including the car it belongs to, the year it was produced, and its name. It is particularly useful in administrative interfaces or anywhere in the application where car model information needs to be collected from the user.

    Attributes:
        car_id (ModelChoiceField): A dropdown selection field for choosing the car instance associated with the model. This field is populated with choices representing all available cars.
        year_id (ModelChoiceField): A dropdown selection field for selecting the year the car model was produced. Choices represent all available years.
        model_name (CharField): A text input field for specifying the name of the car model.
    """

    class Meta:
        model =  CarModel
        fields = ['car_id', 'year_id', 'model_name']


class AddTrimForm(forms.ModelForm):
    """
    A form for adding or updating car trims.

    Associated with the CarTrim model, this form enables users to specify details about a car trim, including its name, the car model it belongs to, the specific car instance, and the production year. It is useful in contexts where detailed information about car trims needs to be collected, such as in inventory management systems or sales platforms.

    Attributes:
        car_trim_name (CharField): A text input field for entering the name of the car trim.
        model_id (ModelChoiceField): A dropdown selection field for choosing the car model associated with the trim. This field is populated with choices representing all available car models.
        car_id (ModelChoiceField): A dropdown selection field for selecting the specific car instance the trim is associated with. Choices represent all available cars.
        year_id (ModelChoiceField): A dropdown selection field for selecting the year the car trim was produced. Choices represent all available years.
    """

    class Meta:
        model =  CarTrim
        fields = ['car_trim_name', 'model_id', 'car_id', 'year_id',]


class AddLocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields =['location_name', 'country_code', 'service_availability']


class AddServiceTypeForm(forms.ModelForm):

    class Meta:
        model = ServiceType
        fields =['service_type_name']


class AddServiceCategoryForm(forms.ModelForm):

    class Meta:
        model = ServiceCategory
        fields =['service_category_name', 'service_type']


class AddServicsForm(forms.ModelForm):

    class Meta:
        model = Services
        fields =['service_title', 'service_description', 'service_category']
        widgets = {
            'content': CKEditor5Widget(config_name='extends'),
        }


class AddSubServiceForm(forms.ModelForm):

    class Meta:
        model = SubServices
        fields = ['service', 'display_text', 'sub_service_title', 'sub_service_description', 'order', 'selection_type', 'optional']