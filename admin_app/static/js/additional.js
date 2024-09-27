document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
});

document.addEventListener('htmx:configRequest', function (event) {
    var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('value');
    console.log('csrfToken', csrfToken);

    if (csrfToken) {
        event.detail.headers['X-CSRFToken'] = csrfToken;
    } else {
        console.error('CSRF token not found in meta tag.');
    }
});

// document.getElementById('sidenav-dropdown-Car-Management').addEventListener('click', function (event) {
//     event.preventDefault();

//     var element = document.getElementById('sidenav-dropdown-menus-Car-Management');

//     if (element.classList.contains('sidenav-menu')) {
//         element.classList.remove('sidenav-menu');
//         element.classList.add('sidenav-menu-show');
//     } else {
//         element.classList.remove('sidenav-menu-show');
//         element.classList.add('sidenav-menu');
//     }
// });


// document.getElementById('sidenav-dropdown-Services-Management').addEventListener('click', function (event) {
//     event.preventDefault();

//     var element = document.getElementById('sidenav-dropdown-menu-Services-Management');
//     console.log('here')

//     if (element.classList.contains('sidenav-menu')) {
//         element.classList.remove('sidenav-menu');
//         element.classList.add('sidenav-menu-show');
//     } else {
//         element.classList.remove('sidenav-menu-show');
//         element.classList.add('sidenav-menu');
//     }
// });

function toggleMenu(menuId) {
    console.log('menuId', menuId);

    var element = document.getElementById(menuId);
    console.log('element', element);


    if (element.classList.contains('sidenav-menu')) {
        element.classList.remove('sidenav-menu');
        element.classList.add('sidenav-menu-show');
    } else {
        element.classList.remove('sidenav-menu-show');
        element.classList.add('sidenav-menu');
    }
}

// document.getElementById('sidenav-dropdown-User-Management').addEventListener('click', function (event) {
//     event.preventDefault();
//     var element = document.getElementById('sidenav-dropdown-menu-User-Management');

//     if (element.classList.contains('sidenav-menu')) {
//         element.classList.remove('sidenav-menu');
//         element.classList.add('sidenav-menu-show');
//     } else {
//         element.classList.remove('sidenav-menu-show');
//         element.classList.add('sidenav-menu');
//     }
// });


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
    console.log('imagediv', imagediv, selectionType);


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
    selectElement.value = status
    serviceTypeNameInput.value = service_type;
    var url = '/admin/service-type/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);
    modal.style.display = 'flex';
}


// Used for the Service category update form data
function updatecategory(formId, id, service_type, service_category_name, status, service_type_instance) {
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
function updateservices(formId, id, service_category, service_title, ispopular, status, service_category_instance, service_description) {


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

    const IspopularInput = modal.querySelector('#Ispopular');
    const IspopularInputOptions = IspopularInput.querySelectorAll('option');
    const IspopularInputopt = IspopularInputOptions[0];
    IspopularInputopt.text = ispopular;
    IspopularInputopt.value = ispopular;

    console.log('service_description', service_description);

    getOrCreateEditor('description', service_description)
        .then(editor => {
            if (editor) {
                // Successfully retrieved or created the editor
                console.log('service_description', service_description);
            }
        });

    modal.style.display = 'flex';

}


const editorsMap = new Map();

// Function to initialize or retrieve an editor by element ID
function getOrCreateEditor(elementId, service_description) {
    const element = document.getElementById(elementId);

    if (!element) {
        console.error(`Element with ID ${elementId} not found.`);
        return Promise.resolve(null); // Return a resolved promise with null
    }

    // Check if an editor is already associated with this element
    if (editorsMap.has(elementId)) {
        const editor = editorsMap.get(elementId);

        editor.setData(service_description); // Set data on the existing editor
        return Promise.resolve(editor); // Return a resolved promise with the editor
    }

    // Create a new editor if it doesn't already exist
    return ClassicEditor
        .create(element)
        .then(editor => {
            editorsMap.set(elementId, editor); // Store the editor instance in the map
            editor.setData(service_description); // Set initial data
            return editor;
        })
        .catch(error => {
            console.error('Error creating the editor:', error);
            return null;
        });
}

// Function to retrieve an editor by element ID
function getEditorById(elementId) {
    return editorsMap.get(elementId) || null;
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

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/car-brand/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const brandNameInput = modal.querySelector('#brand');
    brandNameInput.value = brand;

    const imageurlElement = modal.querySelector('#profile_image');
    imageurlElement.setAttribute('src', image_url);

    modal.style.display = 'flex';

    getOrCreateEditor('description', description)
        .then(editor => {
            if (editor) {
                // Successfully retrieved or created the editor
            }
        });
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


// Used for the car models update form data
function updateCarModel(formId, id, brand, year, model_name, status, brand_instance, year_instance) {

    console.log((formId));
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/car-model/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const serviceTypeNameInput = modal.querySelector('#brand');
    const serviceTypeNameNameOptions = serviceTypeNameInput.querySelectorAll('option');
    const opt = serviceTypeNameNameOptions[0];
    opt.text = brand;
    opt.value = brand_instance;

    const yearNameInput = modal.querySelector('#year');
    const yearNameNameOptions = yearNameInput.querySelectorAll('option');
    const yearopt = yearNameNameOptions[0];
    yearopt.text = year;
    yearopt.value = year_instance;

    const brandNameInput = modal.querySelector('#model_name');
    brandNameInput.value = model_name;

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
) {

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

    const subServiceTitleNameInput = modal.querySelector('#title');
    subServiceTitleNameInput.value = sub_service_title;

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

    modal.style.display = 'flex';

    getOrCreateEditor('description', sub_service_description)
        .then(editor => {
            if (editor) {
                // Successfully retrieved or created the editor
            }
        });
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
    var imagediv = document.getElementById('image_url');

    if (option_type === "Image Type") {
        imagediv.style.display = 'block';
    } else {
        imagediv.style.display = 'none';
    }

    const displayTextNameInput = modal.querySelector('#title');
    displayTextNameInput.value = option_title;

    jsObject = JSON.parse(recommend_inspection_service);

    const selectionTypeNameInput = modal.querySelector('#recommend_inspection_service');
    const selectionTypeNameNameOptions = selectionTypeNameInput.querySelectorAll('input');
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


    const orderNameInput = modal.querySelector('#order');
    orderNameInput.value = order;
    console.log('next_sub_service_instance', next_sub_service_instance);

    const nextSubServiceTypeNameInput = modal.querySelector('#next_sub_service');
    const nextSubServiceNameNameOptions = nextSubServiceTypeNameInput.querySelectorAll('option');
    const nextSubServiceTypeopt = nextSubServiceNameNameOptions[0];
    nextSubServiceTypeopt.text = next_sub_service;
    nextSubServiceTypeopt.value = next_sub_service_instance;

    const statusElement = modal.querySelector('#exampleSelect');
    statusElement.value = status;

    modal.style.display = 'flex';

    getOrCreateEditor('description', option_description)
        .then(editor => {
            if (editor) {
                // Successfully retrieved or created the editor
            }
        });
}



// Used for the User profile detail update
function updateForm(formId, id, first_name, last_name, email, phone_no, is_active, role='user') {

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    
    const url = `/admin/user-management/${id}${role ? '/'+role+'/' : '' }`;
    updateForm.setAttribute('action', url);
    
    const first_nameInput = modal.querySelector('#first_name');
    first_nameInput.value = first_name;

    const last_nameInput = modal.querySelector('#last_name');
    last_nameInput.value = last_name;
    
    const emailInput = modal.querySelector('#email');
    emailInput.value = email;
    
    const phone_noInput = modal.querySelector('#phone_no');
    phone_noInput.value = phone_no;
    
    const is_activeInput = modal.querySelector('#status');
    is_activeInput.value = is_active;
    console.log((formId));

    modal.style.display = 'flex';
}



// Used for the user data update form data
function updateUserProfile(formId, id, first_name, last_name, email, phone_no) {
    
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/user/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const first_nameInput = modal.querySelector('#first_name');
    first_nameInput.value = first_name;

    const last_nameInput = modal.querySelector('#last_name');
    last_nameInput.value = last_name;

    const emailInput = modal.querySelector('#email');
    emailInput.value = email;  

    const phone_noInput = modal.querySelector('#phone_no');
    phone_noInput.value = phone_no;

    modal.style.display = 'flex';
}


// Used for the mechanic details update form data
function updateMechanincForm(formId, id, first_name, last_name, email, phone_no, status, approved) {
    
    console.log('id', status);
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = `/admin/mechanic-management/${parseInt(id)}/`;
    updateForm.setAttribute('action', url);
    

    const first_nameInput = modal.querySelector('#first_name');
    first_nameInput.value = first_name;

    const last_nameInput = modal.querySelector('#last_name');
    last_nameInput.value = last_name;

    const emailInput = modal.querySelector('#email');
    emailInput.value = email;  

    const phone_noInput = modal.querySelector('#phone_no');
    phone_noInput.value = phone_no;

    const statusInput = modal.querySelector("#status");    
    statusInput.value = status;

    const approvedInput = modal.querySelector('#approved');
    approvedInput.value = approved;

    modal.style.display = 'flex';
}

function updateMechanicProfile(formId, id, first_name, last_name, email, phone_no) {
    
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/mechanic/mechanic_dashboard/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const first_nameInput = modal.querySelector('#first_name');
    first_nameInput.value = first_name;

    const last_nameInput = modal.querySelector('#last_name');
    last_nameInput.value = last_name;

    const emailInput = modal.querySelector('#email');
    emailInput.value = email;  

    const phone_noInput = modal.querySelector('#phone_no');
    phone_noInput.value = phone_no;

    modal.style.display = 'flex';
}


function updateAdminProfile(formId, id, first_name, last_name, email, phone_no, status) {
    
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/admin/admin-management/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    const first_nameInput = modal.querySelector('#first_name');
    first_nameInput.value = first_name;

    const last_nameInput = modal.querySelector('#last_name');
    last_nameInput.value = last_name;

    const emailInput = modal.querySelector('#email');
    emailInput.value = email;  

    const phone_noInput = modal.querySelector('#phone_no');
    phone_noInput.value = phone_no;

    if (status){
        const statusInput = modal.querySelector("#status");    
        statusInput.value = status;
    }

    modal.style.display = 'flex';
}


$(document).ready(function () {
    $('#car_brand').change(function () {
        var model1Id = $(this).val();
        console.log('model1Id', model1Id);

        if (model1Id) {
            $.get('/get_caryear_options/', { car_id: model1Id }, function (data) {
                $('#car_year').prop('disabled', false).html('<option value="">Select Year</option>');
                $.each(data, function (index, item) {
                    $('#car_year').append($('<option></option>').attr('value', item.id).text(item.year));
                });
                $('#car_model, #car_trim, ').prop('disabled', true).html('<option value="">Select</option>');
            });
        } else {
            $('#car_year, #car_model, #car_trim, ').prop('disabled', true).html('<option value="">Select</option>');
        }
    });

    $('#car_year').change(function () {
        var model1Id = $('#car_brand').val();
        var model2Id = $(this).val();
        if (model2Id) {
            $.get('/get_carmodel_options/', { car_id: model1Id, year_id: model2Id }, function (data) {
                $('#car_model').prop('disabled', false).html('<option value="">Select Model</option>');
                $.each(data, function (index, item) {
                    $('#car_model').append($('<option></option>').attr('value', item.id).text(item.model_name));
                });
                $('#car_trim, ').prop('disabled', true).html('<option value="">Select</option>');
            });
        } else {
            $('#car_model, #car_trim, ').prop('disabled', true).html('<option value="">Select</option>');
        }
    });

    $('#car_model').change(function () {
        var model1Id = $('#car_brand').val();
        var model2Id = $('#car_year').val();
        var model3Id = $(this).val();
        if (model3Id) {
            $.get('/get_cartrim_options/', {car_id: model1Id, year_id: model2Id, model_id: model3Id }, function (data) {
                $('#car_trim').prop('disabled', false).html('<option value="">Select Trim</option>');
                $.each(data, function (index, item) {
                    $('#car_trim').append($('<option></option>').attr('value', item.id).text(item.car_trim_name));
                });
            });
        } else {
            $('#car_trim, ').prop('disabled', true).html('<option value="">Select</option>');
        }
    });

});



function userCarDetails(formId, image_url, car_brand_detail, car_year_detail, car_model_detail, car_trim_detail, vin_number) {
    
    const modal = document.getElementById(formId);

    const image_urlInput = modal.querySelector('#image_url');
    image_urlInput.setAttribute('src', image_url)
    
    const car_brand_detailInput = modal.querySelector('#car_brand_name');
    car_brand_detailInput.value = car_brand_detail;  

    const car_year_detailInput = modal.querySelector('#car_year_detail');
    car_year_detailInput.value = car_year_detail;
    
    const car_model_detailInput = modal.querySelector('#car_model_name');
    car_model_detailInput.value = car_model_detail;

    const car_trim_detailInput = modal.querySelector('#car_trim_name');
    car_trim_detailInput.value = car_trim_detail;

    const vin_numberInput = modal.querySelector('#vin_number');
    vin_numberInput.value = vin_number;
    
    modal.style.display = 'flex';
}



function userCarDetailsUpdate(formId, id, brand, brand_instance, year, year_instance, model, model_instance, trim, trim_instance, vin) {
    
    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/users-car/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);
    
    const brandInput = modal.querySelector('#brand');
    const brandptions = brandInput.querySelectorAll('option');
    const brandopt = brandptions[0];
    brandopt.text = brand;
    brandopt.value = brand_instance;
    
    const yearInput = modal.querySelector('#year');
    const yearOptions = yearInput.querySelectorAll('option');
    const yearopt = yearOptions[0];
    yearopt.text = year;
    yearopt.value = year_instance;

    const modelInput = modal.querySelector('#model');
    const modelOptions = modelInput.querySelectorAll('option');
    const modelopt = modelOptions[0];
    modelopt.text = model;
    modelopt.value = model_instance;

    const trimInput = modal.querySelector('#trim');
    const trimOptions = trimInput.querySelectorAll('option');
    const trimopt = trimOptions[0];
    trimopt.text = trim;
    trimopt.value = trim_instance;

    const vinInput = modal.querySelector('#vin');
    vinInput.value = vin;
    
    modal.style.display = 'flex';
}


$(document).ready(function () {
    $('#brand').change(function () {
        var model1Id = $(this).val();
        console.log('model1Id', model1Id);

        if (model1Id) {
            $.get('/get_caryear_options/', { car_id: model1Id }, function (data) {
                $('#year').prop('disabled', false).html('<option value="">Select Year</option>');
                $.each(data, function (index, item) {
                    $('#year').append($('<option></option>').attr('value', item.id).text(item.year));
                });
                $('#model, #trim, ').prop('disabled', true).html('<option value="">Select</option>');
            });
        } else {
            $('#year, #model, #trim, ').prop('disabled', true).html('<option value="">Select</option>');
        }
    });

    $('#year').change(function () {
        var model1Id = $('#brand').val();
        var model2Id = $(this).val();
        if (model2Id) {
            $.get('/get_carmodel_options/', { car_id: model1Id, year_id: model2Id }, function (data) {
                $('#model').prop('disabled', false).html('<option value="">Select Model</option>');
                $.each(data, function (index, item) {
                    $('#model').append($('<option></option>').attr('value', item.id).text(item.model_name));
                });
                $('#trim, ').prop('disabled', true).html('<option value="">Select</option>');
            });
        } else {
            $('#model, #trim, ').prop('disabled', true).html('<option value="">Select</option>');
        }
    });

    $('#model').change(function () {
        var model1Id = $('#brand').val();
        var model2Id = $('#year').val();
        var model3Id = $(this).val();
        if (model3Id) {
            $.get('/get_cartrim_options/', {car_id: model1Id, year_id: model2Id, model_id: model3Id }, function (data) {
                $('#trim').prop('disabled', false).html('<option value="">Select Trim</option>');
                $.each(data, function (index, item) {
                    $('#trim').append($('<option></option>').attr('value', item.id).text(item.car_trim_name));
                });
            });
        } else {
            $('#trim, ').prop('disabled', true).html('<option value="">Select</option>');
        }
    });

});