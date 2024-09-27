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
def location_data_handler(request: HttpRequest) -> HttpResponse:
    print('run location')
    """This method is use to render the main page for locations and show the all location's list and status.

    Args:
    -  request: The incoming HTTP request containing all data for show the list of al the saved locations.

    Returns:
    -  Httprequest: This method is use for render the location page with containing all the saved locations.
    """
    try:
        if request.method == 'GET':
            locations_pagination_data = locations_pagination(request)

            context = {
                'curl' : admin_curl,
                'page_obj': locations_pagination_data,
            }
            print('run location1')
            return render(request, 'location/location.html', context)
        
        elif request.method == 'POST':
            form = AddLocationForm(request.POST)

            location_name = request.POST.get('location_name')
            locations_pagination_data = locations_pagination(request)

            context = {
                'curl': admin_curl,
                'page_obj':locations_pagination_data,
            }

            data = {
                "country_code" : request.POST.get('country_code'),
                "location_name" : request.POST.get('location_name'),
                "service_availability" :bool(request.POST.get('service_availability')),
            }
            validate_location_schema(data)
            
            if form.is_valid():
                location = form.save(commit=False)

                token = hashlib.sha256(location_name.encode()).hexdigest()
                location.remember_token = token
                form.save()

                locations_pagination_data = locations_pagination(request)
                context = {
                    'curl':admin_curl,
                    'page_obj':locations_pagination_data,
                }
                messages.success(request, "Added successfully!!!")
                return render(request, 'location/location.html', context)
            
        else:
            messages.error(request, 'Invalid inputs, please try again')
            return redirect('location_data_handler')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
                messages.error(request,schemas.location_schema.location_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return redirect( 'location_data_handler')
            
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect( 'location_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')
    
    except Exception as e:
        print(e)
        messages.error(request, f'{e}')
        return redirect('location_data_handler')   


@login_required
def location_action_handler(request: HttpRequest, id: int) -> HttpResponse:
    """
    Updates the details of a location based on the provided form data.
    
    Args:
    - request (HttpRequest): The incoming HTTP request containing the form data for updating the location.
    - id (int): The unique identifier of the location to be updated.
    
    Returns:
    - HttpResponseRedirect: Redirects to the main location listing page if the update is successful.
    - HttpResponse: Renders the update form template with the submitted data and validation errors if the update fails.
    """
    
    try:
        if request.method == 'POST':
            location = Location.objects.get(id=id)

            data = {
                'location_name': request.POST.get('location_name'),
                'country_code' : request.POST.get('country_code'),
                'service_availability' : bool(request.POST.get('service_availability'),)
            }
            validate_location_schema(data)

            location.status = request.POST.get('status', location.status)
            location.country_code = request.POST.get('country_code', location.country_code)
            location.location_name = request.POST.get('location_name', location.location_name)
            location.service_availability = request.POST.get('service_availability', location.service_availability)
            location.save()

            messages.success(request, 'Updated successfully!')
            return redirect('location_data_handler')
        
        if request.method == 'DELETE':
            location = Location.objects.get(id=id)

            page_obj = locations_pagination(request)
            context = {
                'curl': admin_curl,
                'page_obj':page_obj,
            }

            if location:
                location.delete()

                messages.success(request, f"Delete successfully!!")
                return render(request, 'location/location.html', context, status=200)

    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.location_schema.location_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect( 'location_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect( 'location_data_handler')      
    
    except ObjectDoesNotExist:
        messages.error(request, f'Object not fountd, Try again')
        return redirect('location_data_handler') 
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')            

    except Exception as e:
        messages.error(request, f'{e}')
        return redirect('location_data_handler') 