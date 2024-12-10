from datetime import date
from django.http import HttpRequest
from django.core.paginator import Page
from admin_app.models import ComboDetails
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from user_app.models import UserCarRecord, BookingAndQuote, ServicePayment, UserComboPackage



def User_Car_Record_pagination(request: HttpRequest, user_id) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """
    try:
        User_Car_Record = UserCarRecord.objects.all().order_by('id')
        User_Car_Record = User_Car_Record.filter(user_id=user_id)
        
        # Pagination setup
        paginator = Paginator(User_Car_Record, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj
    
    except ObjectDoesNotExist:
        return None


def User_booking_pagination(request: HttpRequest, id) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """
    try:
        booking = BookingAndQuote.objects.filter(user=id).order_by('-id')
        
        # Pagination setup
        paginator = Paginator(booking, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj
    
    except ObjectDoesNotExist:
        return None


def User_payments_pagination(request: HttpRequest, id) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """
    try:
        payments = ServicePayment.objects.filter(user=id).order_by('-created_at')
        
        # Pagination setup
        paginator = Paginator(payments, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj
    
    except ObjectDoesNotExist:
        return None



def Combos_pagination(request: HttpRequest) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """
    try:
        combos = ComboDetails.objects.all().order_by('-created_at')
        
        for combo in combos:
            if combo.combo_end_date and combo.combo_end_date < date.today():
                combo.status = "Inactive"
                combo.save()
        
        # Pagination setup
        paginator = Paginator(combos, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj
    
    except ObjectDoesNotExist:
        return None


def User_combos_pagination(request: HttpRequest, user) -> Page:
    
    """Paginate a list of all mechanics and return a Page object.

    Args:
    -  request (HttpRequest): The HTTP request object. It is used to access query parameters for mechanics pagination.

    Returns:
    -  page_obj: A Page object containing the paginated mechanics for the mechanics pagination.
    """

    try:
        combos = UserComboPackage.objects.filter(user_id=user).order_by('-created_at')
        
        # Pagination setup
        paginator = Paginator(combos, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj
    
    except ObjectDoesNotExist:
        return None

