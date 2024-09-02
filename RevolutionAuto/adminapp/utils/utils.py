from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from adminapp.models import CarBrand, CarYear, CarModel, CarTrim, Location, ServiceType, ServiceCategory, Services, SubServices

def brand_pagination(request: HttpRequest) -> HttpResponse:

    """Paginate a list of all brands and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for brand pagination.

    Returns:
    -  page_obj: A Page object containing the paginated brands for the brand pagination.
    """
    all_brands = CarBrand.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(all_brands, 10)  # Show 10 brands per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the page object for the requested page

    return page_obj


def year_pagination(request: HttpRequest) -> HttpResponse:
    
    """Paginate a list of all years and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for years pagination.

    Returns:
    -  page_obj: A Page object containing the paginated years for the year pagination.
    """
    caryear = CarYear.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(caryear, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def model_pagination(request: HttpRequest) -> HttpResponse:

    """Paginate a list of all model and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for model pagination.

    Returns:
    -  page_obj: A Page object containing the paginated models for the model pagination.
    """
    caryear = CarModel.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(caryear, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def trim_pagination(request: HttpRequest) -> HttpResponse:

    """Paginate a list of all trims and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for trim pagination.

    Returns:
    -  page_obj: A Page object containing the paginated trims for the trims pagination.
    """
    caryear = CarTrim.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(caryear, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def locations_pagination(request: HttpRequest) -> HttpResponse:
    
    """Paginate a list of all locations and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for location pagination.

    Returns:
    -  page_obj: A Page object containing the paginated locations for the locations pagination.
    """
    Location_1 = Location.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(Location_1, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def service_type_pagination(request: HttpRequest) -> HttpResponse:
    
    """Paginate a list of all service_type and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for service_type pagination.

    Returns:
    -  page_obj: A Page object containing the paginated service_type for the service_type pagination.
    """
    Location_1 = ServiceType.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(Location_1, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def service_category_pagination(request: HttpRequest) -> HttpResponse:
    
    """Paginate a list of all service_category and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for service_category pagination.

    Returns:
    -  page_obj: A Page object containing the paginated service_category for the service_category pagination.
    """
    Location_1 = ServiceCategory.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(Location_1, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def services_pagination(request: HttpRequest) -> HttpResponse:
    
    """Paginate a list of all services and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for services pagination.

    Returns:
    -  page_obj: A Page object containing the paginated services for the services pagination.
    """
    Location_1 = Services.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(Location_1, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def sub_services_pagination(request: HttpRequest) -> HttpResponse:
    
    """Paginate a list of all services and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for services pagination.

    Returns:
    -  page_obj: A Page object containing the paginated services for the services pagination.
    """
    Location_1 = SubServices.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(Location_1, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj