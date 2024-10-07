import os
import html
import json
import schemas
import fastjsonschema
import schemas.service_schema

from django.conf import settings
from admin_app.utils.utils import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.http import (HttpRequest, 
                         HttpResponse, 
                         HttpResponseRedirect)

from admin_app.models import (Services, 
                              SubService, 
                              ServiceType,
                              ServiceCategory,
                              SubServiceOption)

from admin_app.forms import (AddServiceForm,
                             AddSubServiceForm,
                             AddServiceTypeForm, 
                             AddServiceCategoryForm, 
                             AddSubServiceOptionForm)

from schemas.service_schema import (validate_services_details,
                                    validate_sub_service_details,
                                    validate_service_type_details,
                                    validate_service_category_details,
                                    validate_sub_service_option_details)

curl = settings.CURRENT_URL
admin_curl = f"{curl}/admin/"
media_path = f'{settings.MEDIA_URL}' 


# ---------------Service type views---------------

@login_required
def service_type_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying service_type list when the request type is GET and adding a new service_type when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the service_type list. If POST, it processes the logic for adding a new service_type.

        Returns:
            HttpResponse: For GET requests, it returns a response with the service_type list. For POST requests, if the user input is valid, it adds the 
            service_type and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """
    try:
        if request.method == 'GET':

            service_type_pagination_data = service_type_pagination(request)
            context = {
                'curl': admin_curl,
                'page_obj': service_type_pagination_data
            }
            return render(request, 'service/service_type.html', context)
        
        elif request.method == 'POST':
            form = AddServiceTypeForm(request.POST)

            data = {'service_type_name': request.POST.get('service_type_name')}
            validate_service_type_details(data)
            
            if not ServiceType.objects.filter(service_type_name=data.get('service_type_name')):

                if form.is_valid():
                    form.save()

                    service_type_pagination_data = service_type_pagination(request, status=1)
                    context = {
                        'curl': admin_curl,
                        'page_obj':service_type_pagination_data
                    }
                    messages.success(request, "Added Successfully!")
                    return redirect('service_type_data_handler')
                
            else:
                messages.error(request, "This serviece type already exists, try again ")
                return redirect('service_type_data_handler')   
            
        else:
            service_type_pagination_data = service_type_pagination(request, status=1)
            context = {
                'curl':admin_curl,
                'page_obj':service_type_pagination_data
            }
            return render(request, 'service/service_type.html', context)
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.service_type_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', "please enter the valid data"))
        return redirect('service_type_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('service_type_data_handler')

    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('service_type_data_handler')

@login_required
def service_type_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating service_type item when the request type is POST with an ID, and deleting service_type item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the service_type specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'POST':
            service_object = ServiceType.objects.get(id=id)

            data = {'service_type_name': request.POST.get('service_type_name')}
            validate_service_type_details(data)

            if not ServiceType.objects.filter(service_type_name=data.get('service_type_name')).exclude(id=id):
                service_object.status = request.POST.get('status', service_object.status)
                service_object.service_type_name = data.get('service_type_name', service_object.service_type_name)
                service_object.save()

                messages.success(request, "Updated successfully!")
                return redirect('service_type_data_handler')
            
            else:
                messages.error(request, "This serviece type already exists, try again ")
                return redirect('service_type_data_handler')  
        
        elif request.method == 'DELETE':
            service_object = ServiceType.objects.get(id=id)

            if service_object:
                service_object.delete()

                messages.success(request, "Deleted successfully!!")
                return redirect('service_type_data_handler')
            
            else:
                messages.error(request, 'this service type is not found, try again')
                return redirect('service_type_data_handler')
     
        else:
            messages.error(request, f"Unexpected error occur, Try again")
            return redirect('service_type_data_handler')            
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request, schemas.service_schema.service_type_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', "Please enter valid data"))
        return redirect('service_type_data_handler')

    except json.JSONDecodeError as e:
        messages.error(request, f"{e}")
        return redirect('service_type_data_handler')            
    
    except ObjectDoesNotExist:
        messages.error(request, f"Service type does not exist.")
        return redirect('service_type_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')
    
    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('service_type_data_handler')


# ---------------Service category views---------------
@login_required
def service_category_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying service_category list when the request type is GET and adding a new service_category when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the service_category list. If POST, it processes the logic for adding a new service_category.

        Returns:
            HttpResponse: For GET requests, it returns a response with the service_category list. For POST requests, if the user input is valid, it adds the 
            service_category and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """
    try:

        if request.method == 'GET':

            service_category_pagination_data = service_category_pagination(request)
            service_type_pagination_data = service_type_pagination(request, status=1)
            context = {
                'curl': admin_curl,
                'page_obj': service_category_pagination_data,
                'service_type': service_type_pagination_data,
            }
            return render(request, 'service/service_category.html', context) 
        
        elif request.method == 'POST':
            form = AddServiceCategoryForm(request.POST)

            data = {
                'service_type': request.POST.get("service_type"),
                'service_category_name': request.POST.get("service_category_name"),
            }
            validate_service_category_details(data)

            if not ServiceCategory.objects.filter(service_category_name=data.get('service_category_name')):

                if form.is_valid():
                    
                    form.save()
                    service_category_pagination_data = service_category_pagination(request)
                    context = {
                        'curl': admin_curl,
                        'page_obj': service_category_pagination_data,
                    }

                    messages.error(request, 'Added Successfully!!!')
                    return redirect('service_category_data_handler')
            else:
                messages.error(request, "This serviece category already exists, try again ")
                return redirect('service_category_data_handler')  
                
        else:

            service_category_pagination_data = service_category_pagination(request)
            service_type_pagination_data = service_type_pagination(request, status=1)
            context = {
                'curl': admin_curl,
                'page_obj': service_category_pagination_data,
                'service_type': service_type_pagination_data,
            }
            return render(request, 'service/service_category.html', context)
            
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.service_category_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect( 'service_category_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect( 'service_category_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')
    
    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect( 'service_category_data_handler')

@login_required
def service_category_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating service_category item when the request type is POST with an ID, and deleting service_category item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the service_category specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'POST':
            service_category_object = ServiceCategory.objects.get(id=id)

            data = {
                'service_type': request.POST.get('service_type'),
                'service_category_name': request.POST.get('service_category_name')
            }
            validate_service_category_details(data)

            if not ServiceCategory.objects.filter(service_category_name=data.get('service_category_name')).exclude(id=id):     

                # Get old Details and Update Details 
                service_category_object.status = request.POST.get('status', service_category_object.status)
                service_category_object.service_category_name = data.get('service_category_name', service_category_object.service_category_name)
                service_category_object.service_type = ServiceType.objects.get(id=int(data.get('service_type'))) if data.get(
                    "service_type") else ServiceType.objects.get(id=int(service_category_object.service_type.id))
                service_category_object.save()

                messages.success(request, 'Updated successfully!')
                return redirect('service_category_data_handler')
            
            else:
                messages.error(request, "This serviece category already exists, try again ")
                return redirect('service_category_data_handler')  
        
        if request.method == 'DELETE':   
            service_category_object = ServiceCategory.objects.get(id=id)

            if service_category_object:
                service_category_object.delete()

                messages.success(request, f'Delete Successfully')
                return redirect('service_category_data_handler')
            
        else:
            messages.error(request, f"This service category is not found")
            return redirect('service_category_data_handler')
            
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.service_category_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('service_category_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('service_category_data_handler')
        
    except ObjectDoesNotExist:
        messages.error(request, f"Service category does not exist.")
        return redirect('service_category_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')
    
    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('service_category_data_handler')
 

# ---------------Services views---------------

@login_required
def service_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying service list when the request type is GET and adding a new service when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the service list. If POST, it processes the logic for adding a new service.

        Returns:
            HttpResponse: For GET requests, it returns a response with the service list. For POST requests, if the user input is valid, it adds the 
            service and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """
    try:
        if request.method == 'GET':

            services_pagination_data = services_pagination(request)
            service_category_pagination_data = service_category_pagination(request, status=1)
            context = {
                'curl': admin_curl,
                'page_obj': services_pagination_data,
                'service_category': service_category_pagination_data
            }

            return render(request, 'service/services.html', context) 
        
        elif request.method == 'POST':
            form = AddServiceForm(request.POST)

            data = {
                'description': request.POST.get('description'),
                'service_title': request.POST.get('service_title'),
                'service_category': request.POST.get('service_category'),
            }
            validate_services_details(data) 
            
            if not Services.objects.filter(service_title=data.get('service_title')):

                if form.is_valid():
                    form.save()

                    services_pagination_data = services_pagination(request)
                    context = {
                        'curl': admin_curl,
                        'page_obj': services_pagination_data
                    }
                    messages.success(request,"Added successfully!!!")
                    return redirect('service_data_handler')
                else:
                    print(form.errors)
                    return redirect('service_data_handler')
            
            else:
                messages.error(request, "This service already exists, try again ")
                return redirect('service_data_handler')
            
        else:
            services_pagination_data = services_pagination(request)
            service_category_pagination_data = service_category_pagination(request, status=1)

            context = {
                'curl': admin_curl,
                'page_obj': services_pagination_data,
                'service_category': service_category_pagination_data,
            }
            return render(request, 'service/services.html', context) 
            
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.services_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('service_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('service_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')
    
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('service_data_handler')

@login_required
def service_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating service item when the request type is POST with an ID, and deleting service item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the service specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:        
        if request.method == 'POST':
            services_object = Services.objects.get(id=id)

            data = {
                'description':request.POST.get('description'),
                'service_title':request.POST.get('service_title'),
                'service_category':request.POST.get('service_category'),
            }
            validate_services_details(data)

            
            if not Services.objects.filter(service_title=data.get('service_title')).exclude(id=id):
                services_object.status = request.POST.get('status', 1)
                services_object.is_popular = request.POST.get('is_popular')
                services_object.description = data.get('description', services_object.description)
                services_object.service_title = data.get('service_title', services_object.service_title)
                services_object.service_category = ServiceCategory.objects.get(id=int(data.get('service_category'))) if data.get(
                                'service_category') else ServiceCategory.objects.get(id=int(services_object.service_category.id))
                
                services_object.save()
                messages.success(request, 'Update successfully!!')
                return redirect('service_data_handler')
            
            else:
                messages.error(request, "This service already exists, try again ")
                return redirect('service_data_handler')
        
        elif request.method == 'DELETE':
            services_object = Services.objects.get(id=id)

            if services_object:
                services_object.delete()

                messages.success(request, 'Deleted successfully')   
                return redirect('service_data_handler')

            else:
                messages.error(request, f'This service is not found')
                return redirect('service_data_handler')
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.services_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect( 'service_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect( 'service_data_handler')
        
    except ObjectDoesNotExist:
        messages.error(request ,f"Service category does not exist.")
        return redirect('service_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('service_data_handler')

# ---------------Sub-services views---------------
@login_required
def sub_services_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying sub_services list when the request type is GET and adding a new sub_services when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the sub_services list. If POST, it processes the logic for adding a new sub_services.

        Returns:
            HttpResponse: For GET requests, it returns a response with the sub_services list. For POST requests, if the user input is valid, it adds the 
            sub_services and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """

    try:
        if request.method == 'GET':

            sub_services_pagination_data = sub_services_pagination(request)
            services_pagination_data = services_pagination(request, status=1)
            context = {
                'curl': admin_curl,
                'services': services_pagination_data,
                'page_obj': sub_services_pagination_data,
            }
            return render(request, 'service/sub_service.html',context)
        
        elif request.method == 'POST':
            form = AddSubServiceForm(request.POST)

            data = {
                'status': 1,
                'order': request.POST.get('order'),
                'title': request.POST.get('title'),
                'service': request.POST.get('service'),
                'optional': request.POST.get('optional'),
                'description': request.POST.get('description'),
                'display_text': request.POST.get('display_text'),
                'selection_type': request.POST.get('selection_type'),
            }   
            validate_sub_service_details(data)

            if form.is_valid():
                data_validate = SubService.objects.filter(service=data.get('service'), order=data.get('order'), 
                              selection_type=data.get('selection_type'), optional=data.get('optional')).count()
                
                if data_validate == 0:
                    form.save()

                    services_pagination_data = services_pagination(request, status=1)
                    sub_services_pagination_data = sub_services_pagination(request)
                    context = {
                        'curl': admin_curl,
                        'services': services_pagination_data,
                        'page_obj': sub_services_pagination_data,
                    }
                    messages.success(request, 'Added Successful')
                    return redirect('sub_services_data_handler')      
                
                else:
                    messages.error(request, 'Similar record already available, try again')
                    return redirect('sub_services_data_handler')
                
        else:
            services_pagination_data = services_pagination(request)
            sub_services_pagination_data = sub_services_pagination(request)

            context = {
                'curl': admin_curl,
                'services': services_pagination_data,
                'page_obj': sub_services_pagination_data,
            }
            return render(request, 'service/sub_service.html',context)
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.sub_services_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect( 'sub_services_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect( 'sub_services_data_handler')
            
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')
    
    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect( 'sub_services_data_handler')
    

@login_required
def sub_services_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating sub_services item when the request type is POST with an ID, and deleting sub_services item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the sub_services specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """

    try:
        if request.method == 'POST':
            sub_service_object = SubService.objects.get(id=id)

            data = {
                'order': request.POST.get('order'),
                'title': request.POST.get('title'),
                'service': request.POST.get('service'),
                'optional': request.POST.get('optional'),
                'status': int(request.POST.get('status')),
                'description': request.POST.get('description'),
                'display_text': request.POST.get('display_text'),
                'selection_type': request.POST.get('selection_type'),
            }
            validate_sub_service_details(data)    

            data_validate = SubService.objects.filter(service=data.get('service'), order=data.get('order'), 
                selection_type=data.get('selection_type'), optional=data.get('optional')).exclude(id=id).count()
            
            if data_validate == 0 :  

                # Update new or existing dataz
                sub_service_object.order = data.get('order',sub_service_object.order)
                sub_service_object.title = data.get('title', sub_service_object.title)
                sub_service_object.status = data.get('status', sub_service_object.status)
                sub_service_object.optional = data.get('optional', sub_service_object.optional)
                sub_service_object.description = data.get('description', sub_service_object.description)
                sub_service_object.display_text = data.get('display_text',  sub_service_object.display_text)
                sub_service_object.selection_type = data.get('selection_type', sub_service_object.selection_type)
                sub_service_object.service = Services.objects.get(id=int(data.get('service'))) if data.get('service') else Services.objects.get(id=int(sub_service_object.service.id)) 
                sub_service_object.save()

                messages.success(request, 'Update successfully!!')
                return redirect('sub_services_data_handler')
            
            else:
                messages.error(request, 'Same record already available, try again')
                return redirect('sub_services_data_handler')
            
        elif request.method == 'DELETE':
            sub_service_object = SubService.objects.get(id=id)

            if sub_service_object:
                sub_service_object.delete()

                messages.success(request, 'Deleted successfully !')
                return redirect('sub_services_data_handler')
            
            else:
                messages.error(request, 'this sub_service is not found, try again')
                return redirect('sub_services_data_handler')

        else:
            messages.error(request, 'Invalid request, try again')
            return redirect('sub_services_data_handler')
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.sub_services_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect( 'sub_services_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect( 'sub_services_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request ,f"Sub Service does not exist.")
        return redirect('sub_services_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')

    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('sub_services_data_handler')
    
# ---------------Sub-services option views---------------
@login_required
def sub_service_option_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying sub_service_option list when the request type is GET and adding a new sub_service_option when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the sub_service_option list. If POST, it processes the logic for adding a new sub_service_option.

        Returns:
            HttpResponse: For GET requests, it returns a response with the sub_service_option list. For POST requests, if the user input is valid, it adds the 
            sub_service_option and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """
    try:
        if request.method == 'GET':

            inspection_pagination_data = inspection_pagination(request)
            sub_services_pagination_data = sub_services_pagination(request, status=1)
            sub_service_option_pagination_data = sub_service_option_pagination(request)

            context = {
                'inspection': inspection_pagination_data,
                'sub_service': sub_services_pagination_data,
                'page_obj': sub_service_option_pagination_data,
            }

            return render(request,'service/sub_service_option.html', context)
        
        elif request.method == 'POST':
            form = AddSubServiceOptionForm(request.POST, request.FILES)

            option_type = request.POST.get('option_type')
            uploaded_file = request.FILES.get('image_url')

            image_extention = (uploaded_file.name.split('.')[-1].lower() if option_type == "Image Type" and uploaded_file else "")

            data = {
                'option_type': option_type,
                'option_image': image_extention,    
                'order': request.POST.get('order'),
                'title': request.POST.get('title'),
                'description': request.POST.get('description'),
                'sub_service': request.POST.get('sub_service'),
                }
            
            validate_sub_service_option_details(data)

            if (option_type == "Image Type" and uploaded_file) or (option_type == "Text Type"):

                if form.is_valid():
                    subServiceInstance = form.save(commit=False)

                    if uploaded_file:

                        image_url = f'{media_path}option_images/{uploaded_file.name}' 
                        media_directory = os.path.join(settings.BASE_DIR, 'media/option_images')
                        file_path = os.path.join(media_directory, uploaded_file.name)
                        subServiceInstance.image_url = image_url
                        os.makedirs(media_directory, exist_ok=True)

                        with open(file_path, "wb") as fp:
                            for chunk in uploaded_file.chunks():
                                fp.write(chunk)
                    
                    subServiceInstance.save()
                    form.save_m2m()
                    
                    messages.success(request, 'Added successfully!')
                    return redirect('sub_service_option_data_handler')

            else:

                inspection_pagination_data = inspection_pagination(request)
                sub_services_pagination_data = sub_services_pagination(request, status=1)
                sub_service_option_pagination_data = sub_service_option_pagination(request)
                context = {
                        'inspection': inspection_pagination_data,
                        'sub_service': sub_services_pagination_data,
                        'page_obj': sub_service_option_pagination_data,
                    }
                messages.error(request, "Image is not selectd , try again.")
                return render(request,'service/sub_service_option.html', context)
        else:
            inspection_pagination_data = inspection_pagination(request)
            sub_services_pagination_data = sub_services_pagination(request, status=1)
            sub_service_option_pagination_data = sub_service_option_pagination(request)

            context = {
                'page_obj': sub_service_option_pagination_data,
                'inspection': inspection_pagination_data,
                'sub_service': sub_services_pagination_data,
            }
            return render(request,'service/sub_service_option.html', context)
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.sub_services_option_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('sub_service_option_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('sub_service_option_data_handler')

    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('sub_service_option_data_handler')
        

@login_required
def sub_service_option_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating sub_service_option item when the request type is POST with an ID, and deleting sub_service_option item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the sub_service_option specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'POST':
            sub_service_option_object = SubServiceOption.objects.get(id=id)
            form = AddSubServiceOptionForm(request.POST, instance=sub_service_option_object)
    
            option_type = request.POST.get('option_type')
            uploaded_file = request.FILES.get('image_url',sub_service_option_object.image_url)
            image_format = (uploaded_file.name.split('.')[-1].lower() if option_type == "Image Type" and uploaded_file else "")

            if (option_type == "Image Type" and uploaded_file) or (option_type == "Text Type"):

                data = {
                    'option_type': option_type,
                    'option_image': image_format,
                    'order': request.POST.get('order'),
                    'title': request.POST.get('title'),
                    'sub_service': request.POST.get('sub_service'),
                    }
                validate_sub_service_option_details(data)

                if form.is_valid():

                    update_option_form_instance = form.save(commit=False)
                    update_option_form_instance.status = request.POST.get('status',1)

                    if uploaded_file and uploaded_file != sub_service_option_object.image_url:
                        
                        image_name = uploaded_file.name
                        image_url = f'{media_path}/option_images/{image_name}' 
                        media_directory = os.path.join(settings.BASE_DIR, 'media/option_images')
                        file_path = os.path.join(media_directory, image_name)
                        update_option_form_instance.image_url = image_url
                        os.makedirs(media_directory, exist_ok=True)

                        with open(file_path, "wb") as fp:
                            for chunk in uploaded_file.chunks():
                                fp.write(chunk)

                    update_option_form_instance.image_url = "" if option_type == "Text Type" else update_option_form_instance.image_url
                    form.save()
                    
                    messages.success(request, "Updated successfully!")
                    return redirect("sub_service_option_data_handler")
            else:
                messages.error(request, "Image is not selectd , try again.")
                return redirect("sub_service_option_data_handler")
            
        elif request.method == 'DELETE':
            sub_service_option_object = SubServiceOption.objects.get(id=id)
            
            if sub_service_option_object:
                sub_service_option_object.delete()

                messages.success(request, "Deleted successfully!")
                return redirect('sub_service_option_data_handler')
        else:
            messages.error(request, 'Invalid request, try again')
            return redirect("sub_service_option_data_handler")
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.sub_services_option_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('sub_service_option_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('sub_service_option_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request ,f"Sub Service option does not exist.")
        return redirect('sub_service_option_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin/admin_dashboard.html')
    
    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('sub_service_option_data_handler')