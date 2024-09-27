from django.http import HttpRequest
from django.core.paginator import Page
from user_app.models import UserCarRecord
from django.core.paginator import Paginator


def User_Car_Record_pagination(request: HttpRequest) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """
    User_Car_Record = UserCarRecord.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(User_Car_Record, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj