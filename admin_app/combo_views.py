import json
import schemas
import hashlib
import fastjsonschema
import schemas.location_schema
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist 
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from admin_app.utils.utils import Service_combo_pagination
from admin_app.models import ServiceType, Services, ServiceCategory, SubService, ComboDetails, ComboServiceDetails, ComboSubServiceDetails

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
            service_type = ServiceType.objects.all()
            combos = Service_combo_pagination(request)
            context = {
                'curl': curl,
                'page_obj': combos,
                'service_type': service_type,
            }
            return render(request, 'combo/combo_management.html', context)
        
        elif request.method == 'POST':

            with transaction.atomic():
                data = json.loads(request.body)
                print('data', data)
                
                price = data['price']
                end_date = data['end_date']
                comboName = data['comboName']
                start_date = data['start_date']
                discountPrice = data['discountPrice']
                usage_limit = data['usage_limit']
                
                ComboDetail = ComboDetails.objects.create(
                    name = comboName,
                    start_date = start_date,
                    end_date = end_date,
                    price = price,
                    usage_limit = int(usage_limit),
                    discount_price = discountPrice,
                )
                for service  in data['services']:
                    serviceId = Services.objects.get(id=service['serviceId'])
                    serviceType = ServiceType.objects.get(id=service['serviceType'])
                    service_category_id = ServiceCategory.objects.get(id=service['service_category_id'])

                    ComboService = ComboServiceDetails.objects.create(
                        combo = ComboDetail,
                        service = serviceId,
                        service_type = serviceType,
                        service_category = service_category_id,
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
            data = {'messages': message, 'status': 'success'}
            return JsonResponse(data)
            # return redirect('combo_data_handler') 
    
    except ObjectDoesNotExist:
        messages.error(request, f'Object not found, Try again')
        return redirect('combo_data_handler') 
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')            

    except Exception as e:
        messages.error(request, f'{e}')
        return redirect('combo_data_handler') 
    

