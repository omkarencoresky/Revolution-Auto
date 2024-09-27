from django import forms
from admin_app.models import *
from user_app.models import CustomUser
    



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
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password', 'profile_image']


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
        widgets = {
            'description': forms.Textarea(attrs={'required': False}),
        }


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
    """
    A form for adding or updating a Location.

    Associated with the Location model, this form enables users to specify details about a Location, including its name, the country code it belongs to, and service availability. It is useful in contexts where detailed information about locations needs to be collected, such as in inventory management systems or service platforms.

    Attributes:
        location_name (CharField): A text input field for entering the name of the location.
        country_code (CharField): A text input field for entering the country code associated with the location.
        service_availability (BooleanField): A checkbox for indicating the availability of services at this location.
    """

    class Meta:
        model = Location
        fields =['location_name', 'country_code', 'service_availability']


class AddServiceTypeForm(forms.ModelForm):
    """
    A form for adding or updating a Service Type.

    Associated with the ServiceType model, this form allows users to specify the name of a service type. It is useful for categorizing different types of services offered by the system.

    Attributes:
        service_type_name (CharField): A text input field for entering the name of the service type.
    """

    class Meta:
        model = ServiceType
        fields =['service_type_name']


class AddServiceCategoryForm(forms.ModelForm):
    """
    A form for adding or updating a Service Category.

    Associated with the ServiceCategory model, this form enables users to specify the name of a service category and associate it with a service type. This is useful for organizing service offerings in an inventory management system.

    Attributes:
        service_category_name (CharField): A text input field for entering the name of the service category.
        service_type (ModelChoiceField): A dropdown selection field for choosing the service type associated with the category.
    """


    class Meta:
        model = ServiceCategory
        fields =['service_category_name', 'service_type']


class AddServiceForm(forms.ModelForm):
    """
    A form for adding or updating a Service.

    Associated with the Services model, this form allows users to specify details about a service, including its title, description, and associated service category. It is useful for managing service offerings in various contexts.

    Attributes:
        service_title (CharField): A text input field for entering the title of the service.
        description (Textarea): A multi-line text input field for providing a detailed description of the service.
        service_category (ModelChoiceField): A dropdown selection field for choosing the service category associated with the service.
    """


    class Meta:
        model = Services
        fields =['service_title', 'description', 'service_category']
        widgets = {
            'description': forms.Textarea(attrs={'required': False}),
        }


class AddSubServiceForm(forms.ModelForm):
    """
    A form for adding or updating a Sub-Service.

    Associated with the SubService model, this form enables users to specify details about a sub-service, including its title, description, order, and selection type. It is useful in contexts where additional details about services are needed, such as in service catalogs.

    Attributes:
        service (ModelChoiceField): A dropdown selection field for choosing the main service associated with the sub-service.
        display_text (CharField): A text input field for entering the display text of the sub-service.
        title (CharField): A text input field for entering the title of the sub-service.
        description (Textarea): A multi-line text input field for providing a detailed description of the sub-service.
        order (IntegerField): A numeric input field for specifying the order of the sub-service in a list.
        selection_type (CharField): A text input field for specifying the selection type of the sub-service.
        optional (BooleanField): A checkbox for indicating whether the sub-service is optional.
    """


    class Meta:
        model = SubService
        fields = ['service', 'display_text', 'title', 'description', 'order', 'selection_type', 'optional']
        widgets = {
            'description': forms.Textarea(attrs={'required': False}),
        }


class AddSubServiceOptionForm(forms.ModelForm):
    """
    A form for adding or updating a Sub-Service Option.

    Associated with the SubServiceOption model, this form allows users to specify details about options for a sub-service, including its title, description, order, and associated inspection services. It is useful for providing additional choices related to sub-services in service management systems.

    Attributes:
        sub_service (ModelChoiceField): A dropdown selection field for choosing the sub-service associated with the option.
        option_type (CharField): A text input field for specifying the type of the option.
        title (CharField): A text input field for entering the title of the option.
        image_url (URLField): A text input field for providing a URL to an image representing the option.
        order (IntegerField): A numeric input field for specifying the order of the option in a list.
        recommend_inspection_service (ModelMultipleChoiceField): A checkbox selection field for recommending inspection services associated with the option.
        next_sub_service (ModelChoiceField): A dropdown selection field for choosing the next sub-service in a sequence.
        description (Textarea): A multi-line text input field for providing a detailed description of the option.
    """

    recommend_inspection_service = forms.ModelMultipleChoiceField(
        queryset=Inspection.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = SubServiceOption
        fields = ['sub_service', 'option_type', 'title', 'image_url', 'order', "recommend_inspection_service", "next_sub_service", "description"]
        widgets = {
            'description': forms.Textarea(attrs={'required': False}),
        }