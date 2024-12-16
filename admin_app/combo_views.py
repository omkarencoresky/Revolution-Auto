import json
import schemas
import hashlib
import fastjsonschema
import schemas.combo_schema
from datetime import datetime
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from admin_app.models import Notification
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from schemas.combo_schema import validate_add_combo_schema
from admin_app.utils.utils import specific_account_notification
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from admin_app.utils.utils import Service_combo_pagination, Users_combo_pagination
from admin_app.models import ServiceType, Services, ServiceCategory, SubService, ComboDetails, ComboServiceDetails, ComboSubServiceDetails

curl = settings.CURRENT_URL
admin_curl = f"{curl}/admin/"

@login_required
def combo_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """This method is use to render the combo_management page and all operations related to the combo.

    Args:
    -  request: The incoming HTTP request.

    Returns:
    -  Httprequest: This method is use for render combo_management page and all operations related to the combo.
    """
    try:
        if request.method == 'GET':
            service_type = ServiceType.objects.all()
            combos = Service_combo_pagination(request)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            notifications = specific_account_notification(request, request.user.user_id)

            context = {
                'curl': curl,
                'page_obj': combos,
                'service_type': service_type,
                'notifications' : notifications,
                'unread_notification' : unread_notification,
            }
            return render(request, 'combo/combo_management.html', context)
        
        elif request.method == 'POST':

            with transaction.atomic():
                data = json.loads(request.body)
                
                start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
                end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
                
                if end_date < start_date:
                    data = {'messages': 'The end date cannot be earlier than the start date.', 'status': False}
                    return JsonResponse(data)
                
                if ComboDetails.objects.filter(combo_name=data['combo_name']):
                    data = {'messages': 'The same combo name is already used, try again with different Combo Name .', 'status': False}
                    return JsonResponse(data)
                
                validate_add_combo_schema(data)

                ComboDetail = ComboDetails(
                    combo_name = data['combo_name'],
                    combo_start_date = data['start_date'],
                    combo_end_date = data['end_date'],
                    combo_price = data['price'],
                    combo_usage_limit = int(data['usage_limit']),
                    combo_discount_price = data['discount_price'],
                    discount_percentage = data['discount_percentage'],
                )
                ComboDetail.save()

                for service  in data['services']:
                    
                    serviceId = Services.objects.get(id=service['serviceId'])
                    serviceType = ServiceType.objects.get(id=service['serviceType'])
                    service_category_id = ServiceCategory.objects.get(id=service['service_category_id'])

                    ComboService = ComboServiceDetails.objects.create(
                        combo_id = ComboDetail,
                        service_id = serviceId,
                        service_type_id = serviceType,
                        service_category_id = service_category_id,
                    )

                    for subservice in service['sub_services']:
                        sub_service_id = subservice['sub_service_id']

                        options = '' 
                        for option in subservice['sub_service_options']:
                            options += option['sub_service_option_id'] + ','

                        ComboSubServiceDetails.objects.create(
                            combo_service_id = ComboService,
                            sub_service_id = SubService.objects.get(id=sub_service_id),
                            sub_service_option_id = options[:-1]
                        )
            message = ('Combo Created successfully !')
            data = {'messages': message, 'status': True}
            return JsonResponse(data)
        else:
            messages.error(request, 'Something went wrong, try again.')
            return redirect('combo_data_handler')
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        message = schemas.combo_schema.add_combo_schema.get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data')
        data = {'messages': message, 'status': False}
        return JsonResponse(data)
    
    except ObjectDoesNotExist:
        messages.error(request, f'Object not found, Try again')
        return redirect('combo_data_handler') 
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')            

    except Exception as e:
        messages.error(request, 'Something went wrong, try again.')
        return redirect('combo_data_handler') 
    


def users_combo_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """This method is use to render the combo_management page and all operations related to the combo.

    Args:
    -  request: The incoming HTTP request.

    Returns:
    -  Httprequest: This method is use for render combo_management page and all operations related to the combo.
    """
    try:
        if request.method == 'GET':
            combos = Users_combo_pagination(request)
            unread_notification = Notification.get_unread_count(request.user.user_id)
            notifications = specific_account_notification(request, request.user.user_id)

            context = {
                'curl': curl,
                'page_obj': combos,
                'notifications' : notifications,
                'unread_notification' : unread_notification
            }
            return render(request, 'combo/user_combo_management.html', context)
        
        else:
            messages.error(request, 'Something went wrong, try again.')        
            return redirect('combo_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request, f'Object not found, Try again')
        return redirect('combo_data_handler') 
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')            

    except Exception as e:
        messages.error(request, 'Something went wrong, try again.')
        return redirect('combo_data_handler') 
    


