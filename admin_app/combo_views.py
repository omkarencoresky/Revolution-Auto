import json
import schemas
import hashlib
import fastjsonschema
from .models import Location
import schemas.location_schema
from django.conf import settings
from .forms import AddLocationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist 
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from admin_app.utils.utils import locations_pagination
from django.contrib.auth.decorators import login_required
from schemas.location_schema import validate_location_schema

curl = settings.CURRENT_URL
admin_curl = f"{curl}/admin/"

@login_required
def combo_data_handler(request: HttpRequest) -> HttpResponse:
    """This method is use to render the main page for locations and show the all location's list and status.

    Args:
    -  request: The incoming HTTP request containing all data for show the list of al the saved locations.

    Returns:
    -  Httprequest: This method is use for render the location page with containing all the saved locations.
    """
    try:
        if request.method == 'GET':
            context = {
                'curl': curl,
            }
            return render(request, 'combo/combo_management.html', context)
    
    except ObjectDoesNotExist:
        messages.error(request, f'Object not fountd, Try again')
        return redirect('location_data_handler') 
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')            

    except Exception as e:
        messages.error(request, f'{e}')
        return redirect('location_data_handler') 