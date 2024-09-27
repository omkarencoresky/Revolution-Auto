import json
import fastjsonschema
import schemas.car_schema
import schemas.registration_schema

from django.conf import settings
from admin_app.utils.utils import *
from django.contrib import messages
from django.http import JsonResponse
from user_app.forms import AddCarRecord
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.views.decorators.http import require_GET
from user_app.models import CustomUser, UserCarRecord
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from schemas.car_schema import validate_users_car_details
from user_app.utils.utils import User_Car_Record_pagination
from admin_app.models import CarBrand, CarModel, CarTrim, CarYear
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from schemas.registration_schema import validate_update_profile_details_schema

curl = settings.CURRENT_URL+'/'
context = {'curl' : curl}

@never_cache
@login_required
def user_dashboard(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying User dashboard page with the GET request type.

        Args:
            request: The incoming HTTP request. If GET, it shows the User dashboard page

        Returns:
            HttpResponse: For GET requests, it returns a response with the User dashboard page. 
            If the request is invalid, it renders to the home page with an error message and redirects to the main page.
    """
    try:
        if request.method == 'GET':
            context = {
                'curl' : curl
            }
            return render(request, 'user/user_dashboard.html', context)
        
        else:
            return render(request, 'home.html', context)
        
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'home.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect("user_dashboard")
    
@login_required
def user_userapp_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating user details when the request type is POST with an ID, and deleting user profile when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the user profile specified by the ID in the request.
            For DELETE requests, it deletes the user profile specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'POST':
                user_object = CustomUser.objects.get(user_id=id)

                data = {
                    'email': request.POST.get('email',user_object.email),
                    'phone_no': request.POST.get('phone_no', user_object.phone_no),
                    'last_name': request.POST.get('last_name', user_object.last_name), 
                    'first_name': request.POST.get('first_name', user_object.first_name),
                }
                validate_update_profile_details_schema(data)

                user_object.email = data.get('email')
                user_object.phone_no = data.get('phone_no')
                user_object.last_name = data.get('last_name')
                user_object.first_name = data.get('first_name')
                user_object.save()

                messages.success(request, "Updated successfully!")
                return redirect("user_dashboard")
        
        elif request.method == 'DELETE':
            user_object = CustomUser.objects.get(user_id=id)

            if user_object:
                user_object.delete()

                messages.success(request, "Deleted successfully!")
                return redirect( 'user_dashboard')
        
        else:
            return render(request, 'user/user_dashboard.html')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.update_user_detail_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect("user_dashboard")
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect("user_dashboard")
    
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("user_dashboard")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'user_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect("user_dashboard")


def referral_data_handler(request):
    user = request.user
    context = {
        'curl' : curl
    }
    return render(request, 'user/user_referral.html', context)

@login_required
@require_GET
def get_caryear_options(request):

    car_id = request.GET.get('car_id')
    options = CarYear.objects.filter(car_id=car_id).values('id', 'year')
    return JsonResponse(list(options), safe=False)

@login_required
@require_GET
def get_carmodel_options(request):

    car_id = request.GET.get('car_id')
    year_id = request.GET.get('year_id')
    options = CarModel.objects.filter(car_id=car_id, year_id=year_id).values('id', 'model_name')
    return JsonResponse(list(options), safe=False)

@login_required
@require_GET
def get_cartrim_options(request):
    
    car_id = request.GET.get('car_id')
    year_id = request.GET.get('year_id')
    model_id = request.GET.get('model_id')
    options = CarTrim.objects.filter(car_id=car_id, year_id=year_id, model_id=model_id).values('id', 'car_trim_name')

    return JsonResponse(list(options), safe=False)

@login_required
def user_car_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    try:
        if request.method == 'GET':     
            page_obj = User_Car_Record_pagination(request)

            context = {
                'curl' : curl,
                'page_obj': page_obj,
                'model1_options' : CarBrand.objects.all().values('id','brand'),
            }
            return render(request, 'user/user_car.html', context)
        
        elif request.method == 'POST':
            form = AddCarRecord(request.POST)

            vin_num = request.POST.get('vin_number')
            data = {key:request.POST.get(key) for key in ['car_brand', 'car_model', 'car_year', 'car_trim']}

            data['vin_number'] = vin_num if vin_num else ""
            validate_users_car_details(data)  

            unique_record = UserCarRecord.objects.filter(car_brand=data.get('car_brand'),car_model=data.get('car_model'),
                                                         car_year=data.get('car_year'),car_trim=data.get('car_trim'), vin_number=vin_num).exists()
            if not unique_record:
                if form.is_valid():

                    carDetail = form.save(commit=False)
                    carDetail.user_id = request.user
                    carDetail.save()

                    messages.success(request, "Added successful !")
            else:
                messages.error(request, "Similar car details already exist")
            return redirect('user_car_data_handler')

        else:
            page_obj = User_Car_Record_pagination(request)

            context = {
                'curl' : curl,
                'model1_options' : CarBrand.objects.all().values('id','brand'),
                'page_obj': page_obj
            }
            return render(request, 'user/user_car.html', context)
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_schema.users_car_detail_schema.
                       get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect("user_car_data_handler")
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect("user_car_data_handler")
    
    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("user_car_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'user_dashboard.html')

    except Exception as e:
        return redirect('user_car_data_handler')
    

@login_required
def user_car_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    try:
        if request.method == 'POST':

            car_instance = UserCarRecord.objects.get(id=id, )
            form = AddCarRecord(request.POST, instance=car_instance)

            data = {key:request.POST.get(key) for key in ['car_brand', 'car_model', 'car_year', 'car_trim', 'vin_number']}
            validate_users_car_details(data)

            unique_record = UserCarRecord.objects.filter(car_brand=data.get('car_brand'),car_model=data.get('car_model'),
                                                        car_year=data.get('car_year'),car_trim=data.get('car_trim'),
                                                        vin_number=data.get('vin_number')).exists()
            if not unique_record:
                if form.is_valid():

                    form.save()
                    messages.success(request, "Update successfully !")
            else:
                messages.error(request, "Similar car details already exist")
            return redirect('user_car_data_handler')
        
        elif request.method == 'DELETE':
            user_car_instance = UserCarRecord.objects.get(id=id)
            
            if user_car_instance:
                user_car_instance.delete()

                messages.success(request, "Deleted successfully !")
            return redirect("user_car_data_handler")
        
        else:
            return render(request, 'user/user_car.html')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_schema.users_car_detail_schema.
                       get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect("user_car_data_handler")
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect("user_car_data_handler")

    except ObjectDoesNotExist:
        messages.error(request, f"User does not exist.")
        return redirect("user_car_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'user_dashboard.html')

    except Exception as e:
        return redirect('user_car_data_handler')