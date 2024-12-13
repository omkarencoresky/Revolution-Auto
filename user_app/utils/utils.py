import re
from django.http import HttpRequest
from datetime import date, timedelta
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


def convert_to_hours(duration) -> int:
    # If the input is a timedelta, calculate total hours directly
    if isinstance(duration, timedelta):
        return round(duration.total_seconds() / 3600)

    # Otherwise, assume the input is a string
    if isinstance(duration, str):
        # Parse the duration string using a regular expression
        pattern = r"""
            (?:(?P<days>\d+)\s*day[s]?\s*,?\s*)?  # Match 'days' (optional)
            (?P<hours>\d+)\s*:\s*                 # Match 'hours'
            (?P<minutes>\d+)\s*:\s*               # Match 'minutes'
            (?P<seconds>\d+(?:\.\d+)?)            # Match 'seconds'
        """
        match = re.match(pattern, duration, re.VERBOSE)
        
        if not match:
            raise ValueError("Invalid duration format")
        
        # Extract components
        days = int(match.group('days') or 0)
        hours = int(match.group('hours') or 0)
        minutes = int(match.group('minutes') or 0)
        seconds = float(match.group('seconds') or 0)
        
        # Create a timedelta object
        time_diff = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        
        # Calculate total hours
        return round(time_diff.total_seconds() / 3600)
    
    raise TypeError("Input must be a string or timedelta")
