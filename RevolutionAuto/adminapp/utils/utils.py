from adminapp.models import CarBrand, CarYear
from django.core.paginator import Paginator

def brand_pagination(request):
    all_brands = CarBrand.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(all_brands, 10)  # Show 10 brands per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the page object for the requested page
    return page_obj


def year_pagination(request):
    caryear = CarYear.objects.all().order_by('id')
    
    # Pagination setup
    paginator = Paginator(caryear, 10)  # Show 10 brands per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the page object for the requested page
    return page_obj