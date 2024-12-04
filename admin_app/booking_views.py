import os
import json
import schemas
import fastjsonschema
import schemas.booking_schema

from django.conf import settings
from django.db import transaction
from schemas import booking_schema
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache 
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from admin_app.models import ServiceType, ServiceCategory, Services, SubService, SubServiceOption
from admin_app.utils.utils import booking_pagination, Mechanic_pagination, Service_payment_pagination
from user_app.models import BookingAndQuote, CustomUser, SubServiceAndOption, MechanicLeaves, SubServiceBasedOption

curl = settings.CURRENT_URL
EMAIL_HOST_USER = settings.EMAIL_HOST_USER
admin_curl = f"{curl}/admin/"
media_path = f'{settings.MEDIA_URL}'
context = {'curl': curl}


@login_required
def booking_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """This method is use to render the booking page and filter bookings data.

    Args:
        request

    Returns:
        Httprequest: This method is use to render the booking page.
    """
    try:
        if request.method == 'GET':
            status = request.GET.get('status')

            if status != 'None':
                booking_object = booking_pagination(request, status)
            else:
                status = ''
                booking_object = booking_pagination(request, status)

            context = {'curl': curl, 'page_obj': booking_object, 'current_status': status}
            return render(request, 'booking/booking_management.html', context)
        
        else:
            return render(request, 'booking/booking_management.html', context)
    
    except ObjectDoesNotExist:
        messages.error(request)
        return redirect("booking_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_dashboard')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('booking_data_handler')
    

@login_required
def mechanic_data_filter(request:HttpRequest) -> HttpResponse | HttpResponseRedirect:  
    """This method is use to filter the mechanic's data according to there leaves.

    Args:
        request

    Returns:
        Httprequest: This method is use to filter the mechanic's data.
    """
    try:
        date = request.GET.get('date')
        unavailable_mechanic = MechanicLeaves.objects.filter(start_date__lte=date, end_date__gte=date)

        unavailable_mechanic_id = []
        for mechanic in unavailable_mechanic:
            unavailable_mechanic_id.append(mechanic.mechanic_id.user_id)

        options = CustomUser.objects.exclude(user_id__in=unavailable_mechanic_id).filter(role='mechanic')
        options_list = list(options.values())
        return JsonResponse(options_list, safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error','message': 'Invalid date format'}, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No record found with date'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error processing request: {str(e)}'}, status=400)


@login_required
def handle_service_quote_and_mechanic_assignment(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """This method is use to handle the service data and the mechanic assignment.

    Args:
        request

    Returns:
        Httprequest: This method is use to parse service data and the mechanic assignment.
    """
    try:
        if request.method == 'POST':
            quote_object = BookingAndQuote.objects.get(id=id)
            quote_object_service = quote_object.car_services.split(',')
            service_objects = Services.objects.filter(id__in=quote_object_service)
            mechanic = request.POST.get('mechanic')
            
            all_services = ''
            for service in service_objects:
                all_services += service.service_title + ', '

            if request.POST.get('total_service_amount') != None:

                quote_price_data = {'parts_amount' : float(request.POST.get('parts_amount')),
                                'labour_amount' : float(request.POST.get('labour_amount')),
                                'total_service_amount' : float(request.POST.get('total_service_amount'))}
                booking_schema.validate_quote_price(quote_price_data)

                quote_object.total_service_amount = quote_price_data.get('total_service_amount')
                quote_object.labour_amount = quote_price_data.get('labour_amount')
                quote_object.parts_amount = quote_price_data.get('parts_amount')
                quote_object.status = 'quoted'

                quote_object.save() 
                messages.success(request, "Quote send successfully ")

            elif mechanic != None:
                
                mechanic = CustomUser.objects.get(user_id=mechanic)
                quote_object.mechanic = mechanic
                quote_object.status = 'scheduled'
                quote_object.save()

                title = f"Upcoming Service Schedule for {quote_object.car_model.model_name} on {quote_object.schedule_at}, {quote_object.schedule_time_slot}"
                html_content = render_to_string('mechanic/mechanic_booking_mail.html', {'quote_object': quote_object, 
                                                                                        'mechanic': mechanic, 'all_services': all_services})
                plain_message = strip_tags(html_content)
                send_mail(title, plain_message, EMAIL_HOST_USER, [mechanic.email], fail_silently=False,)
                messages.success(request, "Booking scheduled successfully !")

            else:
                messages.error(request, "In-valid Operations")
        else:
            messages.error(request, "In-valid request")

        return redirect('booking_data_handler') 
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request, schemas.booking_schema.quote_price_schema
                       .get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect( 'booking_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect( 'booking_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request)
        return redirect("booking_data_handler")
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_dashboard')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('booking_data_handler')
    

@login_required
def handle_service_status_and_car_details(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """This method is use to handle the service status and handle car details.

    Args:
        request

    Returns:
        Httprequest: This method is use to parse service status and handle car details.
    """
    try:
        if request.method == 'POST':
            quote_object = BookingAndQuote.objects.get(id=id)

            updated_status = request.POST.get('status')
            car_vno = request.POST.get('car_vno')
           

            if quote_object.status != updated_status:
                data = {'status': updated_status}
                booking_schema.validate_car_detail(data)
                quote_object.status = updated_status

                quote_object.save()
                messages.error(request, "Update status successfully ")

            elif car_vno:
                data = {'car_vno': car_vno}
                booking_schema.validate_car_detail(data)
                quote_object.car_vno = car_vno
                quote_object.status = updated_status
                quote_object.save()
                messages.error(request, "Car detail update successfully !")

            else:
                messages.error(request, 'Already updated')

        elif request.method == 'DELETE':
            quote_object = BookingAndQuote.objects.get(id=id)
            booking_object = booking_pagination(request, status=None)
            mechanics = Mechanic_pagination(request)

            if quote_object:
                quote_object.status = 'deleted'

                quote_object.save()
                context = {
                    'curl': curl,
                    'page_obj': booking_object,
                    'mechanics': mechanics
                }
                
                messages.success
                return render(request, 'booking/booking_management.html', context)
        else:
            messages.error(request)
        return redirect('booking_data_handler')
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request, schemas.booking_schema.car_detail_schema
                       .get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect( 'booking_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect( 'booking_data_handler')
    
    except ObjectDoesNotExist:
        messages.error('Booking not found, try again later')
        return redirect("booking_data_handler")
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_dashboard')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('booking_data_handler')


@login_required
def service_update_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """This method is use to handle or update the service details.

    Args:
        request

    Returns:
        Httprequest: This method is use to update the services details.
    """
    try:
        if request.method == 'GET':
            booking_object = BookingAndQuote.objects.get(id=id)
            service_type = ServiceType.objects.all().order_by('id').filter(status=1)
            
            # Get existing services data
            existing_services = []
            if booking_object.car_services:
                service_ids = booking_object.car_services.split(',')

                for service_id in service_ids:
                    try:
                        service = Services.objects.get(id=service_id)
                        service_data = {'serviceId': str(service.id), 'serviceType': str(booking_object.car_service_type.id),
                                    'service_title': service.service_title, 'service_category_id': str(booking_object.car_service_category.id),
                                    'sub_services': []}
                        
                        sub_service_records = SubServiceAndOption.objects.filter(booking_id=booking_object,service_id=service)
                        
                        for sub_service_record in sub_service_records:
                            sub_service_options = SubServiceBasedOption.objects.filter(subServiceAndOptionId=sub_service_record)
                            
                            for sub_service_opt in sub_service_options:
                                sub_service_data = {
                                    'sub_service_id': str(sub_service_opt.sub_service.id),
                                    'sub_service_title': SubService.objects.get(id=sub_service_opt.sub_service.id).title,
                                    'sub_service_options': []}
                                
                                if sub_service_opt.sub_service_option:
                                    option_ids = sub_service_opt.sub_service_option.split(',')

                                    for option_id in option_ids:
                                        try:
                                            option = SubServiceOption.objects.get(id=option_id)
                                            sub_service_data['sub_service_options'].append({
                                                'sub_service_option_id': str(option.id),
                                                'sub_service_option_title': option.title
                                            })
                                        except SubServiceOption.DoesNotExist:
                                            continue
                                
                                service_data['sub_services'].append(sub_service_data)
                        
                        existing_services.append(service_data)
                    except Services.DoesNotExist:
                        continue
                        
            context = {'booking_object': booking_object, 'service_type': service_type, 
                        'existing_services': json.dumps(existing_services)}
            return render(request, 'booking/update_service.html', context)
        
        elif request.method == 'POST':
            
            booking_object = BookingAndQuote.objects.get(id=id)
            data = json.loads(request.body)
            services = data.get('services', [])

            extracted_data = {
                "service_list": [],
                "sub_service_list": [],
                "sub_service_option_list": []
            }
            
            # Extract IDs from the nested structure
            for service in services:
                extracted_data["service_list"].append(service["serviceId"])
                
                if "sub_services" in service:
                    for sub_service in service["sub_services"]:
                        extracted_data["sub_service_list"].append(str(sub_service["sub_service_id"]))
                        
                        if "sub_service_options" in sub_service:
                            for option in sub_service["sub_service_options"]:
                                extracted_data["sub_service_option_list"].append(str(option["sub_service_option_id"]))

            schemas.booking_schema.validate_quote_sub_service_option_data_schema(extracted_data)

            with transaction.atomic():
                # if any part of the code inside this block fails  # (for example, if an exception is raised), all 
                # database changes made within this block will be rolled back, leaving the database in its previous state.

                first_service = services[0]
                service_type_id = first_service.get('serviceType')
                service_category_id = first_service.get('service_category_id')

                try:
                    service_type = ServiceType.objects.get(id=service_type_id, status=1)
                except ServiceType.DoesNotExist:
                    return JsonResponse({'status': 'error',
                                'message': f'Service type with ID {service_type_id} does not exist or is inactive'}, status=400)

                try:
                    service_category = ServiceCategory.objects.get(id=service_category_id, status=1)
                except ServiceCategory.DoesNotExist:
                    return JsonResponse({'status': 'error',
                                'message': f'Service category with ID {service_category_id} does not exist or is inactive'}, status=400)

                service_ids = []
                for service in services:
                    service_id = service.get('serviceId')

                    if service_id:
                        if not Services.objects.filter(id=service_id, status=1).exists():
                            return JsonResponse({'status': 'error',
                                        'message': f'Service with ID {service_id} does not exist or is inactive'}, status=400)
                        service_ids.append(service_id)

                booking_object.car_services = ','.join(service_ids) if service_ids else ''
                booking_object.car_service_type = service_type
                booking_object.car_service_category = service_category
                booking_object.save()

                sub_service_records = SubServiceAndOption.objects.filter(booking_id=booking_object)
                for record in sub_service_records:
                    SubServiceBasedOption.objects.filter(subServiceAndOptionId=record).delete()
                sub_service_records.delete()

                # Create new sub-services and options
                for service in services:
                    service_obj = Services.objects.get(id=service.get('serviceId'))

                    for sub_service in service.get('sub_services', []):
                        sub_service_id = sub_service.get('sub_service_id')
                        options = sub_service.get('sub_service_options', [])

                        if options:
                            sub_service_obj = SubService.objects.get(id=sub_service_id)
                            sub_service_record = SubServiceAndOption.objects.create(booking_id=booking_object, service_id=service_obj)
                            options_str = ','.join([opt['sub_service_option_id'] for opt in options])
                            
                            SubServiceBasedOption.objects.create(subServiceAndOptionId=sub_service_record,sub_service=sub_service_obj,
                                                            sub_service_option=options_str)

            return JsonResponse({'status': 'success', 'message': 'Services updated successfully'})
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        message = schemas.booking_schema.quote_sub_service_option_data_schema.get('properties', {}).get(e.path[1], 
                                                {}).get('description', 'please enter the valid data')
        return JsonResponse({'status': 'success', 'message': message})
        

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_dashboard')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('admin_dashboard')


@login_required
def booking_report_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """This method is use to handle or show the service report data.
    Args:
        request

    Returns:
        Httprequest: This method is use to handle or show the service report data.
    """
    try:
        if request.method == 'GET':
            booking = BookingAndQuote.objects.get(id=id)
            # sub_service_details = get_service_sub_service_and_option(request, id)

            service_detail = SubServiceAndOption.objects.filter(booking_id=id) 
            sub_service_details = {}

            if service_detail:
                for x in service_detail:
                    service_title = x.service_id.service_title
                    service_description = x.service_id.description
                    sub_service_details[service_title] = {'description': service_description,'subservices': []}

                    # Fetch sub-service options for each service
                    sub_Service_detail = SubServiceBasedOption.objects.filter(subServiceAndOptionId=x.id)
                    
                    for y in sub_Service_detail:
                        sub_service = {y.sub_service.display_text: []}

                        for option_id in y.sub_service_option.split(','):
                            sub_Service_option_detail = SubServiceOption.objects.filter(id=option_id)
                            
                            for option in sub_Service_option_detail:
                                sub_service[y.sub_service.display_text].append(option.title)

                        sub_service_details[service_title]['subservices'].append(sub_service)
            else:
                for serviceId in booking.car_services.split(','):
                    serviceObject = Services.objects.get(id=serviceId)
                    sub_service_details[serviceObject.service_title] = {'description': serviceObject.description,'subservices': []}

            context = {'curl': curl, 'booking':booking, 'sub_service_details': sub_service_details}
            return render(request, 'booking/booking_report.html', context)
        
        else:
            return render(request, 'booking/booking_report.html')
    
    except ObjectDoesNotExist:
        messages.error(request, "Object not found!!")
        return redirect("booking_data_handler" )
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_dashboard')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('booking_data_handler')


@login_required
def service_payment_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """This method is use to handle the payment process of the booking.
    Args:
        request

    Returns:
        Httprequest: This method is use to handle the payment process of the booking.
    """
    try:
        if request.method == 'GET':
            all_payment = Service_payment_pagination(request)

            context = {'curl': curl, 'page_obj': all_payment,}
            return render(request, 'booking/payments.html', context)
        
        else:
            all_payment = Service_payment_pagination(request)
            context = {'curl': curl, 'page_obj': all_payment,}
            
            messages.error(request, 'In-valid method, try again')            
            return render(request, 'booking/payments.html', context)

    except ObjectDoesNotExist:
        messages.error(request, "Object not found!!")
        return redirect("booking_data_handler" )
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return redirect('admin_dashboard')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('booking_data_handler')