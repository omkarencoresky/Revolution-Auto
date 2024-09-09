document.addEventListener('htmx:configRequest', function(event) {
    var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('value');
    console.log('csrfToken',csrfToken);
    
    if (csrfToken) {
        event.detail.headers['X-CSRFToken'] = csrfToken;
    } else {
        console.error('CSRF token not found in meta tag.');
    }
});

document.getElementById('sidenav-dropdown-Car-Management').addEventListener('click', function (event) {
    event.preventDefault();

    var element = document.getElementById('sidenav-dropdown-menus-Car-Management');

    if (element.classList.contains('sidenav-menu')) {
        element.classList.remove('sidenav-menu');
        element.classList.add('sidenav-menu-show');
    } else {
        element.classList.remove('sidenav-menu-show');
        element.classList.add('sidenav-menu');
    }
});


document.getElementById('sidenav-dropdown-Services-Management').addEventListener('click', function (event) {
    event.preventDefault();

    var element = document.getElementById('sidenav-dropdown-menu-Services-Management');
    console.log('here')

    if (element.classList.contains('sidenav-menu')) {
        element.classList.remove('sidenav-menu');
        element.classList.add('sidenav-menu-show');
    } else {
        element.classList.remove('sidenav-menu-show');
        element.classList.add('sidenav-menu');
    }
});


document.getElementById('sidenav-dropdown-User-Management').addEventListener('click', function (event) {
    event.preventDefault();
    var element = document.getElementById('sidenav-dropdown-menu-User-Management');

    if (element.classList.contains('sidenav-menu')) {
        element.classList.remove('sidenav-menu');
        element.classList.add('sidenav-menu-show');
    } else {
        element.classList.remove('sidenav-menu-show');
        element.classList.add('sidenav-menu');
    }
});


// For show the add form

function addopenModal(formId) {
    const modal = document.getElementById(formId);
    modal.style.display = 'flex';
}

function closeModal(formId) {
    const modal = document.getElementById(formId);
    modal.classList.add('closing');
    modal.addEventListener('animationend', function () {
        modal.style.display = 'none';
        modal.classList.remove('closing');
    }, { once: true });
}

function closeModalIfOutside(event, formId) {
    if (event.target.id === formId) {
        closeModal(formId);
    }
}


// Use for the image upload input of sub-service option 
function selectionType(id, imageInputId) {
    var selectionType = document.getElementById(id).value;
    var imagediv = document.getElementById(imageInputId);
    console.log('imagediv',imagediv, selectionType);
    

    if (selectionType === "Image Type") {
        imagediv.style.display = 'block';
    } else {
        imagediv.style.display = 'none';
    }
}


// Used for the Service type update form data
function updateopenModal(formId, id, service_type, status) {
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    const serviceTypeNameInput = modal.querySelector('#service_type_name');
    const selectElement = modal.querySelector('#exampleSelect');
    console.log('selectElement', selectElement)
    selectElement.value = status
    serviceTypeNameInput.value = service_type;
    var url = '/admin/service-type/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);
    modal.style.display = 'flex';
}


// Used for the Service category update form data
function updatecategory(formId, id, service_type, service_category_name, status, service_type_instance) {
    console.log('service_type==', service_type_instance)
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');

    const serviceTypeNameInput = modal.querySelector('#service_type');
    const serviceTypeNameNameOptions = serviceTypeNameInput.querySelectorAll('option');
    const opt = serviceTypeNameNameOptions[0];
    opt.text = service_type;
    opt.value = service_type_instance;

    const serviCecategoryNameInput = modal.querySelector('#service_category_name');
    serviCecategoryNameInput.value = service_category_name;

    const selectElement = modal.querySelector('#exampleSelect');
    selectElement.value = status

    var url = '/admin/service-category/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);
    modal.style.display = 'flex';
}


// Used for the Service category update form data
function updateservices(formId, id, service_category, service_title, status, service_category_instance, service_description) {

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/service/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const serviceTypeNameInput = modal.querySelector('#service_category');
    const serviceTypeNameNameOptions = serviceTypeNameInput.querySelectorAll('option');
    const opt = serviceTypeNameNameOptions[0];
    opt.text = service_category;
    opt.value = service_category_instance;

    const servicecategoryNameInput = modal.querySelector('#service_title');
    servicecategoryNameInput.value = service_title;

    const selectElement = modal.querySelector('#exampleSelect');
    selectElement.value = status;

    const serviceDescriptionNameInput = modal.querySelector('#service_description');
    serviceDescriptionNameInput.value = service_description;

    modal.style.display = 'flex';
}


// Used for the Service location update form data
function updatelocation(formId, id, location_name, country_code, status, service_availability) {

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/location/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const locationNameInput = modal.querySelector('#location_name');
    locationNameInput.value = location_name;

    const countryNameInput = modal.querySelector('#country_code');
    countryNameInput.value = country_code;

    const statusElement = modal.querySelector('#exampleSelect');
    statusElement.value = status;

    const availabilityNameInput = modal.querySelector('#service_availability');
    availabilityNameInput.value = service_availability;

    modal.style.display = 'flex';
}



// Used for the car brands update form data
function updateCarBrand(formId, id, brand, description, image_url) {
    console.log('image_url', image_url);

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/car-brand/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const brandNameInput = modal.querySelector('#brand');
    brandNameInput.value = brand;

    const descriptionInput = modal.querySelector('#description');
    descriptionInput.value = description;

    const imageurlElement = modal.querySelector('#profile_image');
    imageurlElement.setAttribute('src', image_url);


    modal.style.display = 'flex';
}


// Used for the car years update form data
function updateCarYear(formId, id, brand, year, status, brand_instance) {

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/car-year/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const serviceTypeNameInput = modal.querySelector('#brand');
    const serviceTypeNameNameOptions = serviceTypeNameInput.querySelectorAll('option');
    const opt = serviceTypeNameNameOptions[0];
    opt.text = brand;
    opt.value = brand_instance;

    const brandNameInput = modal.querySelector('#year');
    brandNameInput.value = year;

    const statusElement = modal.querySelector('#exampleSelect');
    statusElement.value = status;

    modal.style.display = 'flex';
}



// Used for the car trims update form data
function updateCarTrim(formId, id, brand, year, model, trim, status,
    brand_instance, year_instance, model_instance) {

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/car-trim/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const brandTypeNameInput = modal.querySelector('#car_id');
    const brandTypeNameNameOptions = brandTypeNameInput.querySelectorAll('option');
    const brandopt = brandTypeNameNameOptions[0];
    brandopt.text = brand;
    brandopt.value = brand_instance;

    const yearTypeNameInput = modal.querySelector('#year_id');
    const yearTypeNameNameOptions = yearTypeNameInput.querySelectorAll('option');
    const yearopt = yearTypeNameNameOptions[0];
    yearopt.text = year;
    yearopt.value = year_instance;

    const modelTypeNameInput = modal.querySelector('#model');
    const modelTypeNameNameOptions = modelTypeNameInput.querySelectorAll('option');
    const modelopt = modelTypeNameNameOptions[0];
    modelopt.text = model;
    modelopt.value = model_instance;

    const modelNameInput = modal.querySelector('#car_trim');
    modelNameInput.value = trim;

    const statusElement = modal.querySelector('#exampleSelect');
    statusElement.value = status;

    modal.style.display = 'flex';
}


// Used for the car trims update form data
function updateSubServices(formId, id, service_title, display_text, sub_service_title,
    sub_service_description, order, selection_type, optional, status, service_instance,
    selection_type_instance) {


    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/sub-service/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const servicetitleTypeNameInput = modal.querySelector('#service');
    const servicetitleNameNameOptions = servicetitleTypeNameInput.querySelectorAll('option');
    const sTitleopt = servicetitleNameNameOptions[0];
    sTitleopt.text = service_title;
    sTitleopt.value = service_instance;

    const displayTextNameInput = modal.querySelector('#display_text');
    displayTextNameInput.value = display_text;

    const subServiceTitleNameInput = modal.querySelector('#sub_service_title');
    subServiceTitleNameInput.value = sub_service_title;

    const subService_DescriptionNameInput = modal.querySelector('#sub_service_description');
    subService_DescriptionNameInput.value = sub_service_description;

    const orderNameInput = modal.querySelector('#Order');
    orderNameInput.value = order;

    const optionalNameInput = modal.querySelector('#optional');
    const optionalNameNameOptions = optionalNameInput.querySelectorAll('option');
    const optionalopt = optionalNameNameOptions[0];
    optionalopt.text = optional;
    optionalopt.value = optional;

    const selectionTypeNameInput = modal.querySelector('#selection_type');
    const selectionTypeNameNameOptions = selectionTypeNameInput.querySelectorAll('option');
    const selectionTypeopt = selectionTypeNameNameOptions[0];
    selectionTypeopt.text = selection_type;
    selectionTypeopt.value = selection_type;

    const statusElement = modal.querySelector('#exampleSelect');
    statusElement.value = status;

    console.log('optional', selection_type);

    modal.style.display = 'flex';
}



// Used for the car trims update form data
function updateSubServiceOption(formId, id, sub_service_title, option_type, option_title,
    recommend_inspection_service, option_description, order, next_sub_service, status,
    sub_service_instance, next_sub_service_instance) {

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/sub-service-option/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const servicetitleTypeNameInput = modal.querySelector('#sub_service');
    const servicetitleNameNameOptions = servicetitleTypeNameInput.querySelectorAll('option');
    const sTitleopt = servicetitleNameNameOptions[0];
    sTitleopt.text = sub_service_title;
    sTitleopt.value = sub_service_instance;

    const optionalNameInput = modal.querySelector('#option_type');
    const optionalNameNameOptions = optionalNameInput.querySelectorAll('option');
    const optionalopt = optionalNameNameOptions[0];
    optionalopt.text = option_type;
    optionalopt.value = option_type;
    var imagediv = document.getElementById('option_image_update');

    if (option_type === "Image Type"){
        imagediv.style.display = 'block';
    }else {
        imagediv.style.display = 'none';
    }

    const displayTextNameInput = modal.querySelector('#option_title');
    displayTextNameInput.value = option_title;

    jsObject = JSON.parse(recommend_inspection_service);

    const selectionTypeNameInput = modal.querySelector('#recommend_inspection_service');
    const selectionTypeNameNameOptions = selectionTypeNameInput.querySelectorAll('input');
    console.log('selectionTypeNameNameOptions', Array.from(selectionTypeNameNameOptions).length);
    jsObject.forEach(item => {
        inspectionOldId = item.id
        inspectionOldName = item.name
        for (let i = 0; i <= Array.from(selectionTypeNameNameOptions).length; i++) {
            check = Array.from(selectionTypeNameNameOptions)[i];
            check?.removeAttribute('checked');
        }
    });

    jsObject.forEach(item => {
        inspectionOldId = item.id
        inspectionOldName = item.name
        for (let i = 0; i <= Array.from(selectionTypeNameNameOptions).length; i++) {
            check = Array.from(selectionTypeNameNameOptions)[i];
            if (check?.value == inspectionOldId) {
                check?.setAttribute('checked', true)
            }
        }
    });

    const subServiceTitleNameInput = modal.querySelector('#option_description');
    subServiceTitleNameInput.value = option_description;

    const orderNameInput = modal.querySelector('#order');
    orderNameInput.value = order;
    console.log('next_sub_service_instance',next_sub_service_instance);
    
    const nextSubServiceTypeNameInput = modal.querySelector('#next_sub_service');
    const nextSubServiceNameNameOptions = nextSubServiceTypeNameInput.querySelectorAll('option');
    const nextSubServiceTypeopt = nextSubServiceNameNameOptions[0];
    nextSubServiceTypeopt.text = next_sub_service;
    nextSubServiceTypeopt.value = next_sub_service_instance;

    const statusElement = modal.querySelector('#exampleSelect');
    statusElement.value = status;

    modal.style.display = 'flex';
}
