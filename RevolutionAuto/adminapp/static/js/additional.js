document.getElementById('sidenav-dropdown-Car-Management').addEventListener('click', function(event) {
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


document.getElementById('sidenav-dropdown-Services-Management').addEventListener('click', function(event) {
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


document.getElementById('sidenav-dropdown-User-Management').addEventListener('click', function(event) {
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


// Used for the Service type update form data
function updateopenModal(formId, id, service_type, status) {
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    const serviceTypeNameInput =  modal.querySelector('#service_type_name');  
    const selectElement = modal.querySelector('#exampleSelect'); 
    console.log('selectElement',selectElement)
    selectElement.value = status
    serviceTypeNameInput.value = service_type;
    var url = '/admin/service-type/id/'.replace('id', parseInt(id)); 
    updateForm.setAttribute('action', url);
    modal.style.display = 'flex';
}


// Used for the Service category update form data
function updatecategory(formId, id, service_type, service_category_name, status, service_type_instance) {
    console.log('service_type==',service_type_instance)
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');

    const serviceTypeNameInput =  modal.querySelector('#service_type');  
    const serviceTypeNameNameOptions = serviceTypeNameInput.querySelectorAll('option');    
    const opt = serviceTypeNameNameOptions[0];    
    opt.text = service_type;
    opt.value = service_type_instance;

    const serviCecategoryNameInput =  modal.querySelector('#service_category_name');  
    serviCecategoryNameInput.value = service_category_name;

    const selectElement = modal.querySelector('#exampleSelect');
    selectElement.value = status

    var url = '/admin/service-category/id/'.replace('id', parseInt(id)); 
    updateForm.setAttribute('action', url);
    modal.style.display = 'flex';
}   


// Used for the Service category update form data
function updateservices(formId, id, service_category, service_title, status, service_category_instance,service_description) {
        
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/service/id/'.replace('id', parseInt(id)); 
    updateForm.setAttribute('action', url);    
    
    const serviceTypeNameInput =  modal.querySelector('#service_category');  
    const serviceTypeNameNameOptions = serviceTypeNameInput.querySelectorAll('option');    
    const opt = serviceTypeNameNameOptions[0];    
    opt.text = service_category;
    opt.value = service_category_instance;
    
    const servicecategoryNameInput =  modal.querySelector('#service_title');  
    servicecategoryNameInput.value = service_title;

    const selectElement = modal.querySelector('#exampleSelect');
    selectElement.value = status;
    
    const serviceDescriptionNameInput =  modal.querySelector('#service_description');  
    serviceDescriptionNameInput.value = service_description;
    
    modal.style.display = 'flex';
}


// Used for the Service location update form data
function updatelocation(formId, id, location_name, country_code, status, service_availability) {
    
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/location/id/'.replace('id', parseInt(id)); 
    updateForm.setAttribute('action', url);    

    const locationNameInput =  modal.querySelector('#location_name');  
    locationNameInput.value = location_name;
    
    const countryNameInput =  modal.querySelector('#country_code');  
    countryNameInput.value = country_code;
    
    const statusElement = modal.querySelector('#exampleSelect');
    statusElement.value = status;
    
    const availabilityNameInput =  modal.querySelector('#service_availability');  
    availabilityNameInput.value = service_availability;
    
    modal.style.display = 'flex';
}



// Used for the car brands update form data
function updateCarBrand(formId, id, brand, description, image_url) {
    console.log('image_url',image_url);
    
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/car-brand/id/'.replace('id', parseInt(id)); 
    updateForm.setAttribute('action', url);    
    
    const brandNameInput =  modal.querySelector('#brand');  
    brandNameInput.value = brand;
    
    const descriptionInput =  modal.querySelector('#description');  
    descriptionInput.value = description;
    
    const imageurlElement = modal.querySelector('#profile_image');
    imageurlElement.setAttribute('src',image_url); 
    
    
    modal.style.display = 'flex';
}


// Used for the car brands update form data
function updateCarYear(formId, id, brand, year, status,brand_instance) {
    
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/car-year/id/'.replace('id', parseInt(id)); 
    updateForm.setAttribute('action', url);
    
    const serviceTypeNameInput =  modal.querySelector('#brand');  
    const serviceTypeNameNameOptions = serviceTypeNameInput.querySelectorAll('option');    
    const opt = serviceTypeNameNameOptions[0];    
    opt.text = brand;
    opt.value = brand_instance;
    
    const brandNameInput =  modal.querySelector('#year');  
    brandNameInput.value = year;
    
    const statusElement = modal.querySelector('#exampleSelect');
    statusElement.value = status;
    
    modal.style.display = 'flex';
}