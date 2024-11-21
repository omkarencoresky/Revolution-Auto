from admin_app.models import *
from django.http import HttpRequest
from django.core.paginator import Page
from django.core.paginator import Paginator
from user_app.models import CustomUser, BookingAndQuote, Service_payment



def trim_pagination(request: HttpRequest, status=None) -> Page:

    """Paginate a list of all trims and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for trim pagination.

    Returns:
    -  page_obj: A Page object containing the paginated trims for the trims pagination.
    """
    cartrim = CarTrim.objects.all().order_by('id')
    
    if status:
        cartrim = cartrim.filter(status=status)
    # Pagination setup
    paginator = Paginator(cartrim, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def year_pagination(request: HttpRequest, status=None) -> Page:
    
    """Paginate a list of all years and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for years pagination.

    Returns:
    -  page_obj: A Page object containing the paginated years for the year pagination.
    """
    caryear = CarYear.objects.all().order_by('id')
    
    if status:
        caryear = caryear.filter(status=status)
    # Pagination setup
    paginator = Paginator(caryear, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def brand_pagination(request: HttpRequest, status=None) -> Page:

    """Paginate a list of all brands and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for brand pagination.

    Returns:
    -  page_obj: A Page object containing the paginated brands for the brand pagination.
    """
    all_brands = CarBrand.objects.all().order_by('id')

    if status:
        all_brands = all_brands.filter(status=status)   
    # Pagination setup
    paginator = Paginator(all_brands, 10)  # Show 10 brands per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the page object for the requested page

    return page_obj


def model_pagination(request: HttpRequest, status=None) -> Page:

    """Paginate a list of all model and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for model pagination.

    Returns:
    -  page_obj: A Page object containing the paginated models for the model pagination.
    """
    carmodel = CarModel.objects.all().order_by('id')

    if status:
        carmodel = carmodel.filter(status=status)    
    # Pagination setup
    paginator = Paginator(carmodel, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def services_pagination(request: HttpRequest, status=None) -> Page:
    
    """Paginate a list of all services and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for services pagination.

    Returns:
    -  page_obj: A Page object containing the paginated services for the services pagination.
    """
    services = Services.objects.all().order_by('id')
    
    if status:
        services = services.filter(status=status)
    # Pagination setup
    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def locations_pagination(request: HttpRequest, status=None) -> Page:
    
    """Paginate a list of all locations and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for location pagination.

    Returns:
    -  page_obj: A Page object containing the paginated locations for the locations pagination.
    """
    Locations = Location.objects.all().order_by('id')
    
    if status:
        Locations = Locations.filter(status=status)
    # Pagination setup
    paginator = Paginator(Locations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def inspection_pagination(request: HttpRequest, status=None) -> Page:
    
    """Paginate a list of all services and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for services pagination.

    Returns:
    -  page_obj: A Page object containing the paginated services for the services pagination.
    """
    inspection = Inspection.objects.all().order_by('id')
    
    if status:
        inspection = inspection.filter(status=status)
    # Pagination setup
    paginator = Paginator(inspection, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def service_type_pagination(request: HttpRequest, status=None) -> Page:
    
    """Paginate a list of all service_type and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for service_type pagination.

    Returns:
    -  page_obj: A Page object containing the paginated service_type for the service_type pagination.
    """
    service_type = ServiceType.objects.all().order_by('id')
    if status:
        service_type = service_type.filter(status=status)
    
    # Pagination setup
    paginator = Paginator(service_type, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def sub_services_pagination(request: HttpRequest, status=None) -> Page:
    
    """Paginate a list of all services and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for services pagination.

    Returns:
    -  page_obj: A Page object containing the paginated services for the services pagination.
    """
    sub_services = SubService.objects.all().order_by('id')

    if status:
        sub_services = sub_services.filter(status=status)
    # Pagination setup
    paginator = Paginator(sub_services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def service_category_pagination(request: HttpRequest, status=None) -> Page:
    
    """Paginate a list of all service_category and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for service_category pagination.

    Returns:
    -  page_obj: A Page object containing the paginated service_category for the service_category pagination.
    """
    service_category = ServiceCategory.objects.all().order_by('id')
    
    if status:
        service_category = service_category.filter(status=status)
    # Pagination setup
    paginator = Paginator(service_category, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def sub_service_option_pagination(request: HttpRequest, status=None) -> Page:
    
    """Paginate a list of all sub_service_option and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for sub_service_option pagination.

    Returns:
    -  page_obj: A Page object containing the paginated sub_service_option for the sub_service_option pagination.
    """
    sub_service_option = SubServiceOption.objects.all().order_by('id').prefetch_related('recommend_inspection_service')
    
    if status:
        sub_service_option = sub_service_option.filter(status=status)
    # Pagination setup
    paginator = Paginator(sub_service_option, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def user_pagination(request: HttpRequest) -> Page:
    
    """Paginate a list of all sub_service_option and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for sub_service_option pagination.

    Returns:
    -  page_obj: A Page object containing the paginated sub_service_option for the sub_service_option pagination.
    """
    all_user = CustomUser.objects.all().order_by('user_id').filter(role='user')
    
    # Pagination setup
    paginator = Paginator(all_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
    


def admin_pagination(request: HttpRequest) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """
    all_admin = CustomUser.objects.all().order_by('user_id').filter(role='admin')
    
    # Pagination setup
    paginator = Paginator(all_admin, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def all_data(request: HttpRequest, recipient_type) -> Page:

    all = CustomUser.objects.filter(role=recipient_type)
    return all


def specific_account_notification(request: HttpRequest, user_id) -> Page:
    
    all_notifications = Notification.objects.filter(recipient_id=user_id)
    return all_notifications


def referral_pagination(request: HttpRequest) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """
    referral = UserReferral.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(referral, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj



def booking_pagination(request: HttpRequest, status: None) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """

    booking = BookingAndQuote.objects.all().order_by('-created_at')

    if status:
        booking = BookingAndQuote.objects.all().order_by('id').filter(status=status)
    
    # Pagination setup
    paginator = Paginator(booking, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def Mechanic_pagination(request: HttpRequest) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """
    mechanic = CustomUser.objects.filter(role='mechanic').order_by('user_id')
    
    # Pagination setup
    paginator = Paginator(mechanic, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def Service_payment_pagination(request: HttpRequest) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """
    payments = Service_payment.objects.all().order_by('-created_at')
    
    # Pagination setup
    paginator = Paginator(payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj