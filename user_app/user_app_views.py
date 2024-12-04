import os
import json
import hashlib
import fastjsonschema
import schemas.login_schema
import schemas.booking_schema
import schemas.registration_schema

from admin_app.models import *
from django.conf import settings
from admin_app.utils.utils import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from schemas.login_schema import validate_login
from django.template import TemplateDoesNotExist 
from schemas.booking_schema import quote_data_schema
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache 
from schemas.registration_schema import validate_registration
from django.contrib.auth import authenticate, login as auth_login 
from user_app.forms import CustomUserCreationForm, BookingAndQuoteForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from user_app.models import CustomUser, SubServiceAndOption, UserCarRecord, SubServiceBasedOption


curl = settings.CURRENT_URL
media_path = f'{settings.MEDIA_URL}' 

context = {
    'curl': curl
}

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the home.html page for.

    Args:
        request 

    Returns:
        HttpResponse: Home page of our apllication.
    """
    context = {
        'curl': curl
    }
    return render(request, 'home.html', context, status= 200) 

def about(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the about.html page for.

    Args:
        request 

    Returns:
        HttpResponse: About page of our apllication.
    """
    context = {
        'curl': curl
    }
    return render(request, 'about.html', context, status=200)

def service(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the service.html page for.

    Args:
        request 

    Returns:
        HttpResponse: service page of our apllication.
    """
    context = {
        'curl': curl
    }
    return render(request, 'service.html', context, status=200)

def team(request: HttpRequest) -> HttpResponse:
    """
    This function is used for render the team.html page for.

    Args:
        request 

    Returns:
        HttpResponse: team list or details of our apllication.
    """
    context = {
        'curl': curl
    }
    return render(request, 'team.html', context, status=200)

def register(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    If the request is get than it render the register page or if the request is post it apply the user register logic.

    Args:
        request

    Returns:
        HttpResponse: if get request render to the register page if request is post than register the user.
    """
    try:
        if request.method == 'GET':
            form = CustomUserCreationForm()
            referral_token = request.GET.get('referral_token', None)

            context = {
                'curl': curl,
                'form': form,
                'referral_token': referral_token,
                }
            
            return render(request, 'register.html', context, status=200)

        elif request.method == 'POST':
            form = CustomUserCreationForm(request.POST, request.FILES)

            file = request.FILES.get('profile_image')
            file_extension = file.name.split('.')[-1].lower() if file else ""

            data = {key: request.POST.get(key) for key in ['email', 'password', 'phone_no', 'last_name', 'first_name']}
            data['profile_image_extension'] = file_extension
            validate_registration(data)

            if CustomUser.objects.filter(email=data.get('email')).exists():
                messages.error(request, "This email is already registered.")
                return redirect('register')
            
            if data.get('password') == request.POST.get('confirm_password'):
                if form.is_valid():

                    user = form.save(commit=False)  
                    image_url = f'{media_path}profile_images/{file.name}' 
                    media_directory = os.path.join(settings.BASE_DIR, 'media/profile_images')
                    user.profile_image = image_url
                    os.makedirs(media_directory, exist_ok=True)

                    file_path = os.path.join(media_directory, file.name)
                    with open(file_path, "wb") as fp:
                        for chunk in file.chunks():
                            fp.write(chunk)

                    user.email = data.get('email').lower()
                    user.set_password(form.cleaned_data['password'])
                    user.remember_token = hashlib.sha256(data.get('email').lower().encode()).hexdigest()

                    referral_token = CustomUser.objects.filter(remember_token=request.POST.get('referral_token'))
                    if referral_token:
                        email = UserReferral.objects.get(referred_email=(request.POST.get('email').lower()), referrer_id=referral_token.user_id )
                        email.referred_register_status = True
                        email.save()
                        
                    user.save()
                    messages.success(request, "User register successfully!")
                
                else:
                    email_errors = form.errors
                    messages.error(request, f"{email_errors}")
            else:
                messages.error(request, "Password fields do not match.")
            return redirect('register')
        
        else:
            return redirect('register')
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.registration_schema.registration_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', f'please enter the valid data {e}'))
        return redirect('register')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('register')
    
    except ObjectDoesNotExist:
        messages.error(request, f"Please use the same email address for registration that already used in your referral. Thank you!")
        return redirect('register')
    
    except TemplateDoesNotExist:
        # messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('Home')
    
    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('register')

def login(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method is used the credential and validate with fastjsonschema and after that login the 
    user and render it according to the user's access like user, admin, super-admin.

    Args:
        request

    Returns:
        HttpResponse: This method is used for login the user admin, super-admin.
    """
    try:
        if request.method == 'GET':
            
            context = {
                'curl':curl
            }
            return render(request, 'login.html', context, status=200)
        
        elif request.method == 'POST':
            
            User = get_user_model()
            data = {
                'email': request.POST.get('email'),
                'password': request.POST.get('password')
            }   
            validate_login(data)

            user = User.objects.get(email=data.get('email'))
            user = authenticate(request, username=data.get('email'), password=data.get('password')) 

            if user is not None:
                if user.status == 1 and user.approved == 1:
                    auth_login(request, user)
                    if user.role == 'user':
                        return redirect('user_dashboard')
                    
                    elif user.role == 'mechanic':
                        return redirect('mechanic_dashboard')
                    
                    else:
                        return redirect('admin_dashboard')
                    
                else:
                    messages.error(request, "Your account is inactive. Please contact to Admin.")
                    return redirect('Home')
            else:
                messages.error(request, "Invalid email or password. Please try again.")
                return redirect('login')
        else:
            messages.error(request, "Invalid request method")
            return redirect('login')
                
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.login_schema.login_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('login')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('login')
    
    except ObjectDoesNotExist:
        messages.error(request, f"No user found with email")
        return redirect('login')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('Home')
    
    except Exception as e :
        messages.error(request, f"{e}")
        return redirect('login')
    

# @login_required
@require_GET
def get_service_category(request) -> JsonResponse:
    """
    This method is used the get the service category data based on the service type.

    Args:
        request

    Returns:
        HttpResponse: This method is used for get the service category data based on the service type.
    """
    try:
        service_type = request.GET.get('service_type')
        options = ServiceCategory.objects.filter(service_type=service_type).values('id', 'service_category_name')
        return JsonResponse(list(options), safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error','message': 'Invalid service_type data format'}, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No service type found with service_type Id'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error processing request: {str(e)}'}, status=400)



# @login_required
@require_GET
def get_services(request) -> JsonResponse:
    """
    This method is used the get the service data based on the service type.

    Args:
        request

    Returns:
        HttpResponse: This method is used for get the service data based on the service type.
    """
    try:
        service_category = request.GET.get('service_category')
        options = Services.objects.filter(service_category=service_category).values('id', 'service_title')
        return JsonResponse(list(options), safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error','message': 'Invalid service_category data format'}, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No service category found with service_category Id'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error processing request: {str(e)}'}, status=400)


# @login_required
@require_GET
def get_sub_service(request) -> JsonResponse:
    """
    This method is used the get the sub service data based on the service type.

    Args:
        request

    Returns:
        HttpResponse: This method is used for get the sub service data based on the service type.
    """
    try:
        service = request.GET.get('service')
        options = SubService.objects.filter(service=service).values('id', 'title', 'selection_type')
        return JsonResponse(list(options), safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error','message': 'Invalid service data format'}, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No service found with service Id'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error processing request: {str(e)}'}, status=400)


# @login_required
@require_GET
def get_sub_service_option(request) -> JsonResponse:
    """
    This method is used the get the sub service option data based on the service type.

    Args:
        request

    Returns:
        HttpResponse: This method is used for get the sub service option data based on the service type.
    """
    try:
        sub_service = request.GET.get('sub_service')
        options = SubServiceOption.objects.filter(sub_service=sub_service).values('id', 'title')
        return JsonResponse(list(options), safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error','message': 'Invalid sub_service data format'}, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No sub service found with sub_service Id'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error processing request: {str(e)}'}, status=400)



def request_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect | JsonResponse:
    """
    This method is used for process the request a quote data and show the main page.

    Args:
        request

    Returns:
        HttpResponse: This method is used for process the quote request.
    """
    try:
        if request.method == "GET":

            brands = CarBrand.objects.all().order_by('id').filter(status=1)
            locations = Location.objects.all().order_by('id').filter(status=1)
            service_type = ServiceType.objects.all().order_by('id').filter(status=1)

            context = {
                'curl': curl,
                'brands': brands,
                'locations': locations,
                'service_type': service_type,
                'user': request.user
            }
            return render(request, 'service_quote.html', context, status=200)

        elif request.method == "POST":
            
            user_id = request.user.user_id
            user = CustomUser.objects.get(user_id=user_id)

            car_services_data = request.POST.get('car_services')
            services_dict = json.loads(car_services_data)

            # Iterating over the services_dict and extracting subServiceOptions
            sub_service = []
            sub_service_option = []
            
            for service_id, service_data in services_dict.items():
                if 'subServiceOptions' in service_data:

                    for x in service_data['subServiceOptions']:
                        sub_service.append(x['subServiceId'])
                        sub_service_option.append(x['id'])

            quote_data = {
                'service_location': request.POST.get('service_location'),
                'car_brand': request.POST.get('car_brand'),
                'car_year': request.POST.get('car_year'),
                'car_model': request.POST.get('car_model'),
                'car_trim': request.POST.get('car_trim'),
                'car_service_type': request.POST.get('car_service_type'),
                'car_service_category': request.POST.get('car_service_category'),
                'service_list': list(services_dict.keys()),
                'sub_service_list': sub_service,
                'sub_service_option_list': sub_service_option,
            }

            validate = fastjsonschema.compile(quote_data_schema)
            validate(quote_data)
                            
            form_data = request.POST.copy()
            form_data['car_services'] = ','.join(services_dict.keys())
            form = BookingAndQuoteForm(form_data)

            if form.is_valid():
                
                booking = form.save(commit=False)
                booking.user = user
                booking.status = 'pending for quote'
                booking.service_location = Location.objects.get(id=quote_data.get('service_location'))
                booking.car_brand = CarBrand.objects.get(id=quote_data.get('car_brand'))
                booking.car_year = CarYear.objects.get(id=quote_data.get('car_year'))
                booking.car_model = CarModel.objects.get(id=quote_data.get('car_model'))
                booking.car_trim = CarTrim.objects.get(id=quote_data.get('car_trim'))
                booking.car_service_type = ServiceType.objects.get(id=quote_data.get('car_service_type'))
                booking.car_service_category = ServiceCategory.objects.get(id=quote_data.get('car_service_category'))
                booking.car_services = ','.join(services_dict.keys())
                booking.save()

                # Process and save sub-services
                for service_id, service_data in services_dict.items():
                    booking_sub_service = SubServiceAndOption(booking_id=booking, service_id_id=int(service_id))

                    if 'subServiceOptions' in service_data:
                        sub_service_data = {}

                        for option in service_data['subServiceOptions']:

                            if option['subServiceId'] in sub_service_data:
                                sub_service_data[option['subServiceId']].append(option['id'])   

                            else:
                                sub_service_data[option['subServiceId']] = [option['id']]
                        
                        for sub_service_options_object in sub_service_data:
                            sub_service_id = SubService.objects.get(id=sub_service_options_object)

                            if sub_service_id:
                                booking_sub_service.save()
                                
                                SubServiceBasedOption.objects.create(
                                    subServiceAndOptionId=booking_sub_service,
                                    sub_service=sub_service_id,
                                    sub_service_option=','.join(map(str, sub_service_data[sub_service_options_object]))
                                )
                            else:
                                return JsonResponse({'status': 'error', 'field': 'form', 'message': 'Invalid form data'}, status=400)

                return JsonResponse({'status': 'success', 'message': 'Your Quote requested successfully. Wait for the response'})
            else:
                return JsonResponse({'status': 'error', 'field': 'form', 'message': 'Invalid form data'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'field': 'method', 'message': 'Invalid request method'}, status=400)
    
    except json.JSONDecodeError:
        if 'booking' in locals():
            booking.delete()
        return JsonResponse({'status': 'error', 'field': 'car_services', 'message': 'Invalid services data format'}, status=400)
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        error_field = e.path[0] if len(e.path) == 1 else e.path[1]
        message = schemas.booking_schema.quote_data_schema['properties'].get(error_field, {}).get('description', 'Please enter valid data')                    
        return JsonResponse({'status': 'error', 'message': message}, status=400)

    except ObjectDoesNotExist:
        messages.error(request, "No user found with email")
        return redirect('request_data_handler')

    except TemplateDoesNotExist:
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return redirect('Home')

    except Exception as e:
        if 'booking' in locals():
            booking.delete()
        messages.error(request, f"{e}")
        return redirect('request_data_handler')



def booking_service_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect | JsonResponse:
    """
    This method is used for handle the service data on local storage and save a booking.

    Args:
        request

    Returns:
        HttpResponse: This method is used for service data on local storage and save a booking.
    """
    try:
        if request.method == 'GET':

            service_type = ServiceType.objects.all().order_by('id').filter(status=1)
            locations = Location.objects.all().order_by('id').filter(status=1)
            car_details = UserCarRecord.objects.get(id=id)

            context = {'curl': curl, 'car_details': car_details, 'user': request.user, 'locations': locations, 'service_type': service_type,}
            return render(request, 'booking_quote.html', context)
        
        elif request.method == 'POST':

            user_id = request.user.user_id
            user = CustomUser.objects.get(user_id=user_id)

            data = json.loads(request.body)
            car_services = ','.join(data['car_services'].keys())

            # Iterating over the services_dict and extracting subServiceOptions
            sub_service = []
            sub_service_option = []

            for service_id, service_data in data['car_services'].items():
                if 'subServiceOptions' in service_data:
                    for x in service_data['subServiceOptions']:
                        sub_service.append(x['subServiceId'])
                        sub_service_option.append(x['id'])
            
            validate_data = {
                'service_location': data['service_location'],
                'car_brand': data['car_brand'],
                'car_year': data['car_year'],
                'car_model': data['car_model'],
                'car_trim': data['car_trim'],
                'car_service_type': data['car_service_type'],
                'car_service_category': data['car_service_category'],
                'service_list': list(car_services),
                'sub_service_list': sub_service,
                'sub_service_option_list': sub_service_option,
            }

            validate = fastjsonschema.compile(quote_data_schema)
            validate(validate_data)
            
            booking = BookingAndQuote(
                    user=user,
                    status='pending for quote',
                    service_location=Location.objects.get(id=data['service_location']),
                    car_brand=CarBrand.objects.get(id=data['car_brand']),
                    car_model=CarModel.objects.get(id=data['car_model']),
                    car_year=CarYear.objects.get(id=data['car_year']),
                    car_trim=CarTrim.objects.get(id=data['car_trim']),
                    car_vno=data['car_vno'],
                    car_service_type=ServiceType.objects.get(id=data['car_service_type']),
                    car_service_category=ServiceCategory.objects.get(id=data['car_service_category']),
                    car_services=car_services,
                )
            booking.save()
            
            for service_id, service_data in data['car_services'].items():
                bookingSubService=SubServiceAndOption(booking_id=booking, service_id_id=int(service_id))
                bookingSubService.save()

                if 'subServiceOptions' in service_data:
                    sub_service_data = {}

                    for option in service_data['subServiceOptions']:

                        if option['subServiceId']in sub_service_data:
                            sub_service_data[option['subServiceId']].append(option['id'])
                        else:
                            sub_service_data[(option['subServiceId'])] = [option['id']]

                    for subServiceOptionsObject in sub_service_data:
                        if subServiceOptionsObject:

                            sub_service_id = SubService.objects.get(id=subServiceOptionsObject)
                            SubServiceBasedOption.objects.create(subServiceAndOptionId=bookingSubService, sub_service=sub_service_id,
                                                            sub_service_option=','.join(sub_service_data[subServiceOptionsObject])
                                                        )
                        else:
                            return JsonResponse({'status': 'error', 'field': 'form', 'message': 'Invalid form data'})
                        
            return JsonResponse({'status': 'successfully', 'message': 'Your service has been successfully booked. Please wait while we process your request.'})

        else:
            messages.error(request, 'Invalid method')
            return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        error_field = e.path[0] if len(e.path) == 1 else e.path[1]
        message = schemas.booking_schema.quote_data_schema['properties'].get(error_field, {}).get('description', 'Please enter valid data')                    
        return JsonResponse({'status': ' got a error', 'message': message})
    
    except (json.JSONDecodeError, ValueError) as e:
        if 'booking' in locals():
            booking.delete()
        messages.error(request, str(e))
        return JsonResponse({ 'status': 'error', 'message': str(e)})
    
    except TemplateDoesNotExist:
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return redirect('Home')
        
    except ObjectDoesNotExist as e:
        messages.error(request, f"Object not found: {str(e)}")
        return JsonResponse({'status': 'error','message': f"Object not found: {str(e)}"}, status=404)

    except Exception as e:
        messages.error(request, 'An unexpected error occurred')
        return JsonResponse({'status': 'error','message': 'An unexpected error occurred'}, status=500)



def check_login(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method is used for check the user already login or not for process the service booking data.

    Args:
        request

    Returns:
        HttpResponse: This method is used for the user already login or not for process the service booking data.
    """
    try:
        if request.method == 'GET':
            user = request.user

            if str(user) == 'AnonymousUser':
                
                context = {'curl': curl, 'user': user}
                return render(request, 'service_quote_confirmation.html', context)  
            
            elif user.role == 'user':
                
                notifications = specific_account_notification(request, request.user.user_id)
                unread_notification = Notification.get_unread_count(request.user.user_id)
                
                context = {
                    'curl' : curl,
                    'user': request.user,
                    'notifications': notifications,
                    'unread_notification': unread_notification,
                }
                messages.success(request, "Your Quote requested successfully, Wait for the response")
                return render(request, 'user/user_dashboard.html', context)
            
            else:
                return redirect('request_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request)
        return redirect('request_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('Home')
    
    except Exception as e :
        messages.error(request, f"{e}")
        return redirect('request_data_handler')


@never_cache
def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """
    This method is used the logout of user, admin, superadmin with the help of djnago authentication.

    Args:
        request

    Returns:
        HttpResponse: This method is used for logout the user admin, superadmin.
    """
    logout(request)
    messages.success(request, f"logout successfully")
    return redirect('Home')