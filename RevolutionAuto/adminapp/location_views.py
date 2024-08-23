import json
import schemas
import hashlib
import fastjsonschema
from .models import Locations
import schemas.location_schemas
from django.conf import settings
from .forms import ADDLocationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from adminapp.utils.utils import locations_pagination
from schemas.location_schemas import validate_location_schema

curl = settings.CURRENT_URL
admincurl = f"{curl}/adminapp/"


def all_location(request):
    """This method is use to render the main page for locations and show the all location's list and status.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the location page.
    """
    page_obj = locations_pagination(request)

    context = {
        'curl' : admincurl,
        'page_obj': page_obj
    }
    return render(request, 'location/location.html', context)


def display_add_location(request):
    page_obj = locations_pagination(request)

    context = {
        'curl' : admincurl,
        'page_obj': page_obj
    }
    return render (request, 'location/display_add_location.html', context)


def add_location(request):
    try:
        if request.method == 'POST':
            location_name = request.POST.get('location_name')
            form = ADDLocationForm(request.POST)
            page_obj = locations_pagination(request)

            context = {
                'curl': admincurl,
                'page_obj':page_obj,
            }

            try:
                data = {
                    "location_name" : request.POST.get('location_name'),
                    "country_code" : request.POST.get('country_code'),
                    "service_availability" :bool(request.POST.get('service_availability'))
                }
                validate_location_schema(data)
                
                if form.is_valid():
                    location = form.save(commit=False)
                    token = hashlib.sha256(location_name.encode()).hexdigest()
                    location.remember_token = token
                    form.save()

                    page_obj = locations_pagination(request)

                    context = {
                        'curl':admincurl,
                        'page_obj':page_obj,
                    }
                    messages.success(request, "Added successfully!!!")
                    return render(request, 'location/location.html', context)
                else:
                    messages.error(request, 'Invalid inputs, please try again')
                    return redirect ('get_all_locations')
                
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                print('here2')
                messages.error(request,schemas.location_schemas.location_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return redirect ( 'get_all_locations')
            
            except json.JSONDecodeError:
                print('here3')
                messages.error(request, f"{e}")
                return redirect ( 'get_all_locations')
            
            except ObjectDoesNotExist:
                print('here1')
                messages.error(request, f'{e}')
                return redirect ('get_all_locations')
            
    except Exception as e:
        print('here4')
        return redirect ('get_all_locations')
    

@csrf_exempt
def delete_location(request, id):
    try:
        page_obj = locations_pagination(request)

        context = {
            'curl': admincurl,
            'page_obj':page_obj,
        }
        location = Locations.objects.get(id=id)

        if location:
            location.delete()
            messages.success(request, f"{location.location_name} is deleted successfully!!")
            return render(request, 'location/location.html', context, status=200)
        
    except ObjectDoesNotExist:
        messages.error(request, f"{location.location_name} does not exist. try again")
        return render(request, 'location/location.html', context)

    except Exception:
        messages.error(request, 'Unexpected action, try again')
        return render(request, 'location/location.html', context)
    

def update_location(request, id):
    
    try:
        if request.method == 'GET':
            location1 = locations_pagination(request)
            location = Locations.objects.get(id=id)
            context = {
                'curl': admincurl,
                'page_obj' : location1,
                'location' : location,
            }
            print('here1post')

            return render(request, 'location/update_location.html', context)
        
        if request.method == 'POST':
            location = Locations.objects.get(id=id)
            form = ADDLocationForm(request.POST)
            context = {
                'curl':admincurl,
                'location':location,
            }
            try:
                data = {
                    'location_name': request.POST.get('location_name'),
                    'country_code' : request.POST.get('country_code'),
                    'service_availability' : request.POST.get('service_availability'),
                }
                validate_location_schema(data)

                location.status = request.POST.get('status', location.status)
                location.country_code = request.POST.get('country_code', location.country_code)
                location.location_name = request.POST.get('location_name', location.location_name)
                location.service_availability = request.POST.get('service_availability', location.service_availability)

                location.save()
                messages.success(request, 'Updated successfully!')
                return redirect('get_all_locations')

            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                print('here2')
                messages.error(request,schemas.location_schemas.location_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return redirect ( 'get_all_locations')
            
            except json.JSONDecodeError:
                print('here3')
                messages.error(request, f"{e}")
                return redirect ( 'get_all_locations')
            
            except ObjectDoesNotExist:
                print('here1')
                messages.error(request, f'{e}')
                return redirect ('get_all_locations') 

    except Exception as e:
        print('here')
        return redirect('get_all_locations') 