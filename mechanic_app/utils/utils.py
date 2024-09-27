from admin_app.models import *
from django.http import HttpRequest
from user_app.models import CustomUser
# from mechanic_app.models import Mechanic
from django.core.paginator import Page
from django.core.paginator import Paginator




def mechanic_pagination(request: HttpRequest) -> Page:
    
    """Paginate a list of all sub_service_option and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for sub_service_option pagination.

    Returns:
    -  page_obj: A Page object containing the paginated sub_service_option for the sub_service_option pagination.
    """
    all_mechanic = CustomUser.objects.all().order_by('user_id').filter(role='mechanic')
    
    # Pagination setup
    paginator = Paginator(all_mechanic, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


