let currentServiceId = null;
let selectedServices = {};

document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
});

document.addEventListener('htmx:configRequest', function (event) {
    var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('value');

    if (csrfToken) {
        event.detail.headers['X-CSRFToken'] = csrfToken;
    } else {
        console.error('CSRF token not found in meta tag.');
    }
});



function toggleMenu(menuId) {
    var element = document.getElementById(menuId);

    if (element.classList.contains('sidenav-menu')) {
        element.classList.remove('sidenav-menu');
        element.classList.add('sidenav-menu-show');
    } else {
        element.classList.remove('sidenav-menu-show');
        element.classList.add('sidenav-menu');
    }
}


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

    getOrCreateEditor('description', service_description)
        .then(editor => {
            if (editor) {
                // Successfully retrieved or created the editor
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
function updateForm(formId, id, first_name, last_name, email, phone_no, is_active, role = 'user') {

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');

    const url = `/admin/user-management/${id}${role ? '/' + role + '/' : ''}`;
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

    if (status) {
        const statusInput = modal.querySelector("#status");
        statusInput.value = status;
    }

    modal.style.display = 'flex';
}


$(document).ready(function () {
    $('#car_brand').change(function () {
        var model1Id = $(this).val();

        if (model1Id) {
            $.get('/get-caryear-options/', { car_id: model1Id }, function (data) {
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
            $.get('/get-carmodel-options/', { car_id: model1Id, year_id: model2Id }, function (data) {
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
            $.get('/get-cartrim-options/', { car_id: model1Id, year_id: model2Id, model_id: model3Id }, function (data) {
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



function userNotifications(formId, id, title, message, email, is_read) {

    const modal = document.getElementById(formId);

    const titleInput = modal.querySelector('#title');
    titleInput.value = title;

    const messageInput = modal.querySelector('#message');
    messageInput.value = message;


    const emailInput = modal.querySelector('#email');
    emailInput.value = email;

    modal.style.display = 'flex';
}



function userCarDetailsUpdate(formId, id, brand, brand_instance, year, year_instance, model, model_instance, trim, trim_instance, vin) {

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form');
    var url = '/user-cars/id/'.replace('id', parseInt(id));
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
        

        if (model1Id) {
            $.get('/get-caryear-options/', { car_id: model1Id }, function (data) {
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
            $.get('/get-carmodel-options/', { car_id: model1Id, year_id: model2Id }, function (data) {
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
            $.get('/get-cartrim-options/', { car_id: model1Id, year_id: model2Id, model_id: model3Id }, function (data) {
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



function handleUserTypeChange() {
    const userTypeSelect = document.getElementById('user_type');
    const sentToSelect = document.getElementById('sent_to');
    const emailInput = document.getElementById('addemail');


    if (userTypeSelect.value === "") {
        // If no user type is selected, disable both Sent To and Email
        sentToSelect.disabled = true;
        emailInput.disabled = true;
    } else {
        // If a user type is selected, enable Sent To but keep Email disabled
        sentToSelect.disabled = false;
        emailInput.setAttribute('disabled', true);
        emailInput.value = ""; // Clear email input when enabling/disabling
    }
}

function handleSentToChange() {
    const sentToSelect = document.getElementById('sent_to');
    const emailInput = document.getElementById('addemail');

    if (sentToSelect.value === "specific") {
        // If "Specific" is selected, enable Email input
        emailInput.disabled = false;
    } else {
        // If "All" is selected or no selection, disable Email input
        emailInput.disabled = true;
        emailInput.value = ""; // Clear email input when disabling
    }
}

// Initial setup
function initializeForm() {
    handleUserTypeChange();
    handleSentToChange();
}

// Call initializeForm when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initializeForm);


function redirectToNotification(url) {
    window.location.href = url;
    
}


function hideShowDropdown(event, layerId, elementId) {
    // Prevent event from bubbling up
    event.stopPropagation();
    

    const layerElement = document.getElementById(layerId);
    const childElement = document.getElementById(elementId);

    if (!layerElement.classList.contains("show")) {
        layerElement.classList.add("show");
        childElement.classList.add("show");
    } else {
        layerElement.classList.remove("show");
        childElement.classList.remove("show");
    }
}


document.addEventListener('DOMContentLoaded', function() {
    // Initialize location selection
    const locationSelect = document.getElementById('location');
    const locationMessage = document.querySelector('.location-message');
    const confirmLocationBtn = document.getElementById('confirm-location');

    locationSelect.addEventListener('change', function() {
        if (this.value) {
            locationMessage.textContent = `Great! We have certified mobile mechanics in ${this.options[this.selectedIndex].text}`;
            confirmLocationBtn.classList.remove('hidden');
            confirmLocationBtn.classList.add('nextButton');

        } else {
            locationMessage.textContent = '';
            confirmLocationBtn.classList.add('hidden');
        }
    });

    // Handle tab navigation
    const tabs = document.querySelectorAll('[role="tab"]');
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            // Update tab states
            tabs.forEach(t => {
                t.setAttribute('aria-selected', 'false');
                t.querySelector('a').classList.remove('active');
            });
            this.setAttribute('aria-selected', 'true');
            this.querySelector('a').classList.add('active');
        });
    });
});


function showServiceSection() {
        const locationSelect = document.getElementById('location');
        const confirmButton = document.getElementById('confirm-location');
        const locationMessage = document.querySelector('.location-message');
        const serviceContainer = document.getElementById('service-container');
        
        if (locationSelect.value) {
            // Show car selection section
            // Show the service container
            serviceContainer.classList.remove('hidden');
            // Update the location confirmation message
            locationMessage.textContent = 'Location confirmed!';
            locationMessage.classList.add('success');
            confirmButton.classList.add('hidden');
        } else {
            locationMessage.textContent = 'Please select a location.';
            locationMessage.classList.remove('success');
        }
    }


// Location Section Handling
function showDiv() {
    const locationSelect = document.getElementById('location');
    const carSelection = document.getElementById('car_selection');
    const confirmButton = document.getElementById('confirm-location');
    const locationMessage = document.querySelector('.location-message');
    
    if (locationSelect.value) {
        carSelection.classList.remove('hidden');
        locationMessage.textContent = 'Location confirmed!';
        locationMessage.classList.add('success');
        confirmButton.classList.add('hidden');
    }
}

// Show confirm button when location is selected
document.getElementById('location').addEventListener('change', function() {
    const confirmButton = document.getElementById('confirm-location');
    if (this.value) {
        confirmButton.classList.remove('hidden');
    } else {
        confirmButton.classList.add('hidden');
    }
});

// Brand Selection
function addBrandId(event, is_combo) {
    const target = event.target;
    const year_selection = document.getElementById('year_selection');
    const model_selection = document.getElementById('model_selection');
    const trim_selection = document.getElementById('trim_selection');
    // const nextStepButton = document.getElementById('nextStepButtonForService');

    // Reset any existing brand selection
    const activeElement = document.querySelector('#brand');
    if (activeElement) {
        activeElement.removeAttribute('id');
    }

    // Set new selection
    target.setAttribute('id', 'brand');
    
    // Reset and hide dependent selections
    model_selection.innerHTML = '';
    model_selection.classList.add('hidden');
    trim_selection.innerHTML = '';
    trim_selection.classList.add('hidden');
    // nextStepButton.classList.add('hidden');

    // Show year selection and fetch options
    year_selection.classList.remove('hidden');
    onBrandChange(target, is_combo);
}

// Year Selection
function onBrandChange(target, is_combo) {
    const brandId = target.value;
    const yearSelection = document.getElementById('year_selection');

    if (brandId) {
        fetch(`/get-caryear-options/?car_id=${brandId}`)
            .then(response => response.json())
            .then(data => {
                yearSelection.innerHTML = '';
                
                if (data.length > 0) {
                    yearSelection.innerHTML = '<label class="summary-heading">Select Your Car Year</label>';
                    data.forEach(item => {
                        yearSelection.innerHTML += `
                            <label class="car-options">
                                <input type="radio" name="year" value="${item.id}" onchange="addYearId(event, ${brandId}, ${is_combo})">
                                <div class="custom-radio">${item.year}</div>
                            </label>
                        `;
                    });
                } else {
                    yearSelection.innerHTML = '<label class="summary-heading">No year options available</label>';
                }
            })
            .catch(error => console.error('Error fetching car years:', error));
    }
}

// Model Selection
function addYearId(event, car_id, is_combo) {
    const target = event.target;
    const model_selection = document.getElementById('model_selection');
    const trim_selection = document.getElementById('trim_selection');
    // const nextStepButton = document.getElementById('nextStepButtonForService');

    // Reset any existing year selection
    const activeElement = document.querySelector('#year');
    if (activeElement) {
        activeElement.removeAttribute('id');
    }
    target.setAttribute('id', 'year');
    
    trim_selection.innerHTML = '';
    trim_selection.classList.add('hidden');
    // nextStepButton.classList.add('hidden');

    model_selection.classList.remove('hidden');
    onYearChange(target, car_id, is_combo);
}

function onYearChange(year, car_id, is_combo) {
    const yearId = year.value;
    const modelSelection = document.getElementById('model_selection');

    if (yearId) {
        fetch(`/get-carmodel-options/?car_id=${car_id}&year_id=${yearId}`)
            .then(response => response.json())
            .then(data => {
                modelSelection.innerHTML = '';
                
                if (data.length > 0) {
                    modelSelection.innerHTML = '<label class="summary-heading">Select Your Car Model</label>';
                    data.forEach(item => {
                        modelSelection.innerHTML += `
                            <label class="car-options">
                                <input type="radio" name="model" value="${item.id}" onchange="addModelId(event, ${yearId}, ${car_id}, ${is_combo})">
                                <div class="custom-radio">${item.model_name}</div>
                            </label>
                        `;
                    });
                } else {
                    modelSelection.innerHTML = '<label class="summary-heading">No model options available</label>';
                }
            })
            .catch(error => console.error('Error fetching car models:', error));
    }
}

// Trim Selection
function addModelId(event, year_id, car_id, is_combo) {
    const target = event.target;
    const trim_selection = document.getElementById('trim_selection');
    // const nextStepButton = document.getElementById('nextStepButtonForService');

    // Reset any existing model selection
    const activeElement = document.querySelector('#model');
    if (activeElement) {
        activeElement.removeAttribute('id');
    }

    // Set new selection
    target.setAttribute('id', 'model');
    
    // Reset next step button
    // nextStepButton.classList.add('hidden');

    // Show trim selection and fetch options
    trim_selection.classList.remove('hidden');
    onModelChange(target, car_id, year_id, is_combo);
}

function onModelChange(model, car_id, year_id, is_combo) {
    const modelId = model.value;
    const trimSelection = document.getElementById('trim_selection');

    if (modelId) {
        fetch(`/get-cartrim-options/?car_id=${car_id}&year_id=${year_id}&model_id=${modelId}`)
            .then(response => response.json())
            .then(data => {
                trimSelection.innerHTML = '';
                
                if (data && data.length > 0) {
                    trimSelection.innerHTML = '<label class="summary-heading">Select Your Car Trim</label>';
                    data.forEach(item => {
                        trimSelection.innerHTML += `
                            <label class="car-options">
                                <input type="radio" name="trim" value="${item.id}" onchange="showNextStep('nextStepButtonForService', ${is_combo})">
                                <div class="custom-radio">${item.car_trim_name}</div>
                            </label>
                        `;
                    });
                    trimSelection.innerHTML += `<div style="padding: 30px 10px; text-align: end; width: 100%;">
                        <button type="button" class="hidden" id="nextStepButtonForService">Submit <i class="fas fa-arrow-right"></i></button>
                    </div>`
                } else {
                    trimSelection.innerHTML = '<label class="summary-heading">No trim options available</label>';
                }
            })
            .catch(error => console.error('Error fetching car trims:', error));
    }
}

// Next Step Button
function showNextStep(id, is_combo) {
    const nextStepButton = document.getElementById(id);
    nextStepButton.classList.remove('hidden');

    // Add click handler for next step button
    if (!is_combo){
        document.getElementById(id).addEventListener('click', function() {
            id==='nextStepButtonForFinal' ? displayFinalSummary() :  displaySelectionSummary();  
        });    
    }
}


//-----------------------------for Service Type--------------------------------

function addServiceTypeId(event) {
    const target = event.target;
    
    // Reset any existing brand selection
    const activeElement = document.querySelector('#service_type');
    if (activeElement) {
        activeElement.removeAttribute('id');
    }

    // Set new selection
    target.setAttribute('id', 'service_type');        
    onServiceCategoryChange(target);
}



//-----------------------------for Service category --------------------------------

// Year Selection
function onServiceCategoryChange(target) {
    const serviceType = target.value;
    const serviceCategorySelection = document.getElementById('service_category_selection');

    if (serviceType) {
        
        fetch(`/get-service-category/?service_type=${serviceType}`)
            .then(response => response.json())
            .then(data => {
                serviceCategorySelection.innerHTML = '';
                
                if (data.length > 0) {
                    serviceCategorySelection.innerHTML = '<label class="summary-heading">Select Service Category </label>';
                    data.forEach(item => {
                        serviceCategorySelection.innerHTML += `
                            <label class="car-options">
                                <input type="radio" name="service_category" value="${item.id}" onchange="addServiceCategory(event)">
                                <div class="custom-radio">${item.service_category_name}</div>
                            </label>
                        `;
                    });
                } else {
                    serviceCategorySelection.innerHTML = '<label class="summary-heading">No year options available</label>';
                }
            })
            .catch(error => console.error('Error fetching car years:', error));
    }
}


function addServiceCategory(event) {
    const target = event.target;
    
    // Reset any existing brand selection
    const activeElement = document.querySelector('#service_category');
    if (activeElement) {
        activeElement.removeAttribute('id');
    }

    // Set new selection
    // onServiceCategoryChange(target);
    target.setAttribute('id', 'service_category');    
    onServices(target);    
}


//-----------------------------for Services--------------------------------

// Services Selection
function onServices(target) {
    const serviceCategory = target.value;
    const servicesSelection = document.getElementById('services_selection');
    

    if (serviceCategory) {
        fetch(`/get-services/?service_category=${serviceCategory}`)
            .then(response => response.json())
            .then(data => {
                servicesSelection.innerHTML = '';
                
                if (data.length > 0) {
                    servicesSelection.innerHTML = '<label class="summary-heading">Select Services </label>';
                    data.forEach(item => {
                        servicesSelection.innerHTML += `
                            <label class="car-options">
                                <input type="radio" name="services" value="${item.id}" onchange="addServices(event)">
                                <div class="custom-radio">${item.service_title}</div>
                            </label>
                        `;
                    });
                } else {
                    servicesSelection.innerHTML = '<label class="summary-heading">No year options available</label>';
                }
            })
            .catch(error => console.error('Error fetching car years:', error));
    }
}

function addServices(event) {
    const target = event.target;
    
    // Reset any existing brand selection
    const activeElement = document.querySelector('#services');
    if (activeElement) {
        activeElement.removeAttribute('id');
    }

    // Set new selection
    target.setAttribute('id', 'services'); 
    document.getElementById('addMore').classList.remove('hidden');
    onSubService(target);
    showNextStep('nextStepButtonForFinal');
}

//-----------------------------for Sub Service--------------------------------

function onSubService(target) {
    const service = target.value;
    const subServicesSelection = document.getElementById('sub_service_selection');    

    if (service) {
        fetch(`/get-sub-service/?service=${service}`)
            .then(response => response.json())
            .then(data => {
                subServicesSelection.innerHTML = '';
                
                if (data.length > 0) {
                    subServicesSelection.innerHTML = '<label class="summary-heading">Select Sub Service</label>';
                    
                    const subServicesContainer = document.createElement('div');
                    subServicesContainer.className = 'sub-services-container';
                    subServicesContainer.classList.add('d-flex', 'justify-content-evenly', 'w-100');
                    
                    // Process each sub-service
                    data.forEach(item => {
                        const serviceBlock = document.createElement('div');
                        serviceBlock.className = 'service-block mb-4';
                        
                        // Add the sub-service title
                        serviceBlock.innerHTML = `
                            <label class="mb-2" style="width:100%;">
                                <div class="custom-radio">
                                    <span value="${item.id}" class="font-semibold" class="sub-service" name="sub-service" >${item.title}</span>
                                    <div id="options-${item.id}" class="options-container pl-8"></div>
                                </div>
                            </label>
                        `;
                        
                        // Fetch options for this sub-service
                        fetch(`/get-sub-service-option/?sub_service=${item.id}`)
                            .then(response => response.json())
                            .then(data => {
                                const options = Array.isArray(data) ? data : data.options || [];
                                // Check title to determine if multiple selection is needed
                                const selectionType = item.title.toLowerCase().includes('one or more') ? 'multiple' : 'single';
                                const optionsContainer = serviceBlock.querySelector(`#options-${item.id}`);
                                
                                if (options && options.length > 0) {
                                    options.forEach(option => {
                                        const optionElement = document.createElement('div');
                                        optionElement.className = 'option-item my-2';
                                        
                                        // Always use checkbox for "one or more" selections
                                        const inputType = selectionType === 'multiple' ? 'checkbox' : 'radio';
                                        const inputName = selectionType === 'multiple' 
                                            ? `option_multiple_${item.id}` 
                                            : `option_single_${item.id}`;
                                        
                                        optionElement.innerHTML = `
                                            <label class="flex items-center">
                                                <input type="${inputType}" 
                                                       name="sub_service_option" 
                                                       value="${option.id}"
                                                       class="mr-2"
                                                       onchange="handleOptionSelection(this, '${selectionType}')">
                                                <span>${option.title}</span>
                                            </label>
                                        `;
                                        optionsContainer.appendChild(optionElement);
                                    });
                                } else {
                                    optionsContainer.innerHTML = '<p class="text-gray-500">No options available</p>';
                                }
                            })
                            .catch(error => console.error('Error fetching options:', error));
                        
                        subServicesContainer.appendChild(serviceBlock);
                    });
                    
                    subServicesSelection.appendChild(subServicesContainer);
                } else {
                    subServicesSelection.innerHTML = '<label class="summary-heading">No sub-services available</label>';
                }
            })
            .catch(error => console.error('Error fetching sub-services:', error));
    }
}

// Unified handler for both single and multiple selections
function handleOptionSelection(input, selectionType) {
    const subServiceElement = input.closest('.custom-radio').querySelector('.font-semibold');
    const subServiceparent = input.closest('.option-item');
    
    
    const subServiceTitle = subServiceElement.textContent;
    
    if (selectionType === 'multiple') {
        if (!handleMultipleSelection(input)) {
            return;
        }
        
        // For multiple selection, add/remove data attributes
        if (input.checked) {
            input.dataset.subService = subServiceTitle;
            input.classList.add('sub_service_checked');
            subServiceparent.classList.add('sub_service_parent');
        } else {
            delete input.dataset.subService;
            input.classList.remove('sub_service_checked');
            subServiceparent.classList.remove('sub_service_parent');
        }
    } else {
        // Handle single selection (radio buttons)
        const container = input.closest('.options-container');
        const allRadios = container.querySelectorAll('input[type="radio"]');
        
        allRadios.forEach(radio => {
            
            if (radio !== input) {
                radio.checked = false;
                radio.classList.remove('sub_service_checked');
                radio.closest('.option-item').classList.remove('sub_service_parent');
                delete radio.dataset.subService;
            }
        });
        
        if (input.checked) {
            input.dataset.subService = subServiceTitle;
            input.classList.add('sub_service_checked');
            subServiceparent.classList.add('sub_service_parent');

        } else {
            delete input.dataset.subService;
            input.classList.remove('sub_service_checked');
            subServiceparent.classList.remove('sub_service_parent');
        }
    }
    
    addSubServices({
        target: input,
        type: 'change'
    });
}

// Helper function to handle multiple selection logic
function handleMultipleSelection(checkbox) {
    
    const parentContainer = checkbox.closest('.options-container');    
    const allCheckboxes = parentContainer.querySelectorAll('input[type="checkbox"]');
    const maxSelections = 10;
    
    // Count selected checkboxes
    const selectedCount = Array.from(allCheckboxes)
        .filter(cb => cb.checked)
        .length;
    
    // If too many selections, uncheck the last one
    if (selectedCount > maxSelections) {
        checkbox.checked = false;
        alert(`You can only select up to ${maxSelections} positions`);
        return false;
    }
    return true;
}


function addSubSersubServiceElementIdvices(event) {
    // Used for adding the sub-service ids
    const target = event.target;
    const isChecked = event.target.checked;
    
    // Reset any existing brand selection
    if (isChecked) {    
        target.classList.add('sub_service_checked'); // Add highlight
    } else {
        target.classList.remove('sub_service_checked'); // Remove highlight
    }
}


//-----------------------------Display displaySelectionSummary--------------------------------

function displaySelectionSummary() {
    
    
    const selections = {
        location: document.getElementById('location'),
        brand: document.querySelector('input[name="brand"][id="brand"]'),
        year: document.querySelector('input[name="year"][id="year"]'),
        model: document.querySelector('input[name="model"][id="model"]'),
        trim: document.querySelector('input[name="trim"]:checked')
    };
      
    const summaryContainer = document.getElementById('selection-summary');
    const summaryHTML = `
        <div class="summary-content">
            <label class="summary-heading">Selected Vehicle Details</label>
            <div class="summary-grid">
                <div class="summary-item">
                    <h3>Location</h3>
                    <p>${selections.location.options[selections.location.selectedIndex].text}</p>
                </div>
                <div class="summary-item">
                    <h3>Car Make</h3>
                    <p>${selections.brand ? selections.brand.parentNode.querySelector('.custom-radio').textContent : 'Not selected'}</p>
                </div>
                <div class="summary-item">
                    <h3>Year</h3>
                    <p>${selections.year ? selections.year.parentNode.querySelector('.custom-radio').textContent : 'Not selected'}</p>
                </div>
                <div class="summary-item">
                    <h3>Model</h3>
                    <p>${selections.model ? selections.model.parentNode.querySelector('.custom-radio').textContent : 'Not selected'}</p>
                </div>
                <div class="summary-item">
                    <h3>Trim</h3>
                    <p>${selections.trim ? selections.trim.parentNode.querySelector('.custom-radio').textContent : 'Not selected'}</p>
                </div>
            </div>
            <button type="button" onclick="editSelections()" class="edit-button">Edit Details</button>
        </div>
    `;

    summaryContainer.innerHTML = summaryHTML;
    summaryContainer.classList.remove('hidden');


    document.getElementById('car-location').classList.add('steps-complete');
    document.getElementById('car-location').classList.remove('steps-incomplete');

    document.getElementById('car-services').classList.add('steps-incomplete');
    document.getElementById('service-container').classList.remove('hidden');
    
    // Hide the selection form
    document.getElementById('car-location-section').classList.add('hidden');
    
}

function editSelections() {
    // Hide summary
    document.getElementById('selection-summary').classList.add('hidden');
    document.getElementById('nextStepButtonForFinal').classList.add('hidden');
    document.getElementById('addMore').classList.add('hidden');

    document.getElementById('car-location').classList.remove('steps-complete');
    document.getElementById('car-location').classList.add('steps-incomplete');

    document.getElementById('services').classList.remove('steps-incomplete');
    document.getElementById('service-container').classList.add('hidden');
    // Show selection form
    document.getElementById('car-location-section').classList.remove('hidden');
}

let result = {}

function storeCurrentData() {
    const selections = {
        service_type: document.querySelector('input[name="service_type"]:checked'),
        service_category: document.querySelector('input[name="service_category"]:checked'),
        services: document.querySelector('input[name="services"]:checked'),
        sub_service_options: document.querySelectorAll('input[name="sub_service_option"]:checked')
    };

    function getSelectionsData(selections) {
        const selectedServiceId = selections.services?.value;

        const subServiceOptions = Array.from(selections.sub_service_options).map(option => ({
            subService: option.closest('.custom-radio').querySelector('.font-semibold').textContent,
            subServiceId: option.closest('.custom-radio').querySelector('.font-semibold').getAttribute('value'),
            id: option.value,
            text: option.nextElementSibling.textContent
        }));
        
        return {
            serviceType: {
                id: selections.service_type?.value,
                serviceTypetext:selections.service_type.closest('.car-options').querySelector('.custom-radio').textContent,
                serviceCategory: {
                    id: selections.service_category?.value,
                    serviceCategorytext:selections.service_category.closest('.car-options').querySelector('.custom-radio').textContent,
                    services: {
                        [selectedServiceId]: {
                            servicestext:selections.services.closest('.car-options').querySelector('.custom-radio').textContent,
                            subServiceOptions
                        },
                    },
                },
            },
        };
    }

    const selectionsData = getSelectionsData(selections);

    if (Object.keys(result).length > 0) {
        const existingServiceId = selectionsData.serviceType.serviceCategory.services[selections.services.value];

        // Append new subServiceOptions to the existing array
        if (result.serviceType.serviceCategory.services[existingServiceId]) {
            const existingOptions = result.serviceType.serviceCategory.services[existingServiceId].subServiceOptions;
            const newOptions = selectionsData.serviceType.serviceCategory.services[existingServiceId].subServiceOptions;

            // Create a map to track unique options by text
            const optionMap = new Map();
            existingOptions.forEach(option => optionMap.set(option.text, option.id));
            newOptions.forEach(option => optionMap.set(option.text, option.id)); // This will overwrite existing ids if same text

            // Convert the map back to an array
            result.serviceType.serviceCategory.services[existingServiceId].subServiceOptions = Array.from(optionMap.entries()).map(([text, id]) => ({ text, id }));
        } else {
            // If services are different, add the new service entry
            result.serviceType.serviceCategory.services[selections.services.value] = {
                subServiceOptions: selectionsData.serviceType.serviceCategory.services[selections.services.value].subServiceOptions,
                servicestext:selections.services.closest('.car-options').querySelector('.custom-radio').textContent,
            };
        }
    } else {
        // Fresh result, assign selectionsData
        result = selectionsData;
    }
    // console.log('result', result);
    clearSelections()
    
}

//  clearSelections

function clearSelections() {
    const elements = [
        'input[name="service_type"]:checked',
        'input[name="service_category"]:checked',
        'input[name="services"]:checked',
        'input[name="sub_service_option"]:checked'
    ];

    elements.forEach(selector => {
        const selected = document.querySelectorAll(selector);
        selected.forEach(element => {
            element.checked = false;
        });
    });
}



function displayFinalSummary() {
    // Call storeCurrentData to ensure result is up to date
    storeCurrentData();

    const serviceSummaryContainer = document.getElementById('service-selection-summary');

    // Build sub-services HTML
    let subServicesHtml = '';
    const storedServices = result.serviceType?.serviceCategory?.services || {}; 

    // Create a map to combine sub-services
    const subServiceMap = {};

    // Process stored services
    Object.entries(storedServices).forEach(([key, service]) => {
        
        const subServiceOptions = service?.subServiceOptions || [];

        subServiceOptions.forEach(option => {
            const { subService, text } = option;
            if (!subServiceMap[subService]) {
                subServiceMap[subService] = []; // Create an array for this subService if it doesn't exist
            }
            subServiceMap[subService].push(text); // Add the option text to the corresponding subService
        });
    });

    // Generate HTML for combined sub-services
    Object.entries(subServiceMap).forEach(([subService, options]) => {
        subServicesHtml += `
            <div class="sub-service-group mb-3 border-b pb-2">
                <h6 class="font-semibold text-gray-800">${subService}</h6>
                <ul class="pl-4 mt-2 w-100" style="display: block; margin:0px;">
                    ${options.map(optionText => `<li class="text-gray-600 mb-1"><div>• ${optionText}</div></li>`).join('')}
                </ul>
            </div>
        `;
    });

    // Build summary HTML with improved structure
    const summaryHTML = `
        <div class="summary-content p-4 bg-white rounded-lg shadow">
            <label class="summary-heading text-xl font-bold mb-4 block">Selected Service Details</label>
            <div class="summary-grid grid gap-4">
                <div class="summary-item">
                    <h3 class="text-lg font-semibold text-gray-800">Service Type</h3>
                    <p class="text-gray-600">• ${result.serviceType?.serviceTypetext || 'Not selected'}</p>
                </div>
                <div class="summary-item">
                    <h3 class="text-lg font-semibold text-gray-800">Service Category</h3>
                    <p class="text-gray-600">• ${result.serviceType?.serviceCategory?.serviceCategorytext || 'Not selected'}</p>
                </div>
                <div class="summary-item">
                    <h3 class="text-lg font-semibold text-gray-800">Services</h3>
                    <ul class="text-gray-600" style="display:block; margin:0px;">
                        ${Object.values(storedServices).map(service => `<li>• ${service.servicestext}.</li>`).join('')}
                    </ul>
                </div>
                ${subServicesHtml ? `
                    <div class="summary-item">
                        <h3 class="text-lg font-semibold text-gray-800">Selected Options</h3>
                        <div class="mt-2">${subServicesHtml}</div>
                    </div>
                ` : ''}
            </div>
        </div>
    `;

    // Update the summary container with the generated HTML
    serviceSummaryContainer.innerHTML = summaryHTML;    
    serviceSummaryContainer.classList.remove('hidden');

    // Update UI states
    document.getElementById('car-location').classList.add('steps-complete');
    document.getElementById('car-location').classList.remove('steps-incomplete');

    document.getElementById('car-services').classList.add('steps-complete');
    document.getElementById('car-services').classList.remove('steps-incomplete');

    document.getElementById('nextStepButtonForFinal').classList.add('hidden');
    document.getElementById('addMore').classList.add('hidden');
    document.getElementById('car-review').classList.add('steps-incomplete');

    document.getElementById('formButtons').classList.remove('hidden');
    
    // Hide the selection forms
    document.getElementById('selection-summary').classList.add('hidden');
    document.getElementById('service-container').classList.add('hidden');
}

// hide Location Section
function hideLocationSection(Id){
    if (Id){
        document.getElementById(Id).classList.add('hidden')
    }
}


// Update addSubServices to maintain the selection state
function addSubServices(event) {
    const target = event.target;
    const isChecked = target.checked;
    
    if (isChecked) {
        target.classList.add('sub_service_checked');    
    } else {
        target.classList.remove('sub_service_checked');
    }
}


function editServiceSelections() {
    // Hide summaries
    document.getElementById('formButtons').classList.add('hidden');
    document.getElementById('services').classList.add('steps-incomplete');
    document.getElementById('car-location').classList.add('steps-incomplete');
    document.getElementById('service-selection-summary').classList.add('hidden');
    
    document.getElementById('addMore').classList.remove('hidden');
    document.getElementById('services').classList.remove('steps-complete'); // Reset step indicators
    document.getElementById('service-container').classList.remove('hidden'); // Show selection forms
    document.getElementById('selection-summary').classList.remove('hidden');
    document.getElementById('car-location').classList.remove('steps-complete');   // Reset step indicators
    document.getElementById('nextStepButtonForFinal').classList.remove('hidden');
    document.getElementById('car-selection-container').classList.remove('hidden');
}


//------------------- Used for save details in local storage for service------------------------

function selectedCredential() {
        
    const selections = {
        service_location: document.querySelector('select[name="location"]').value,
        car_brand: document.querySelector('input[name="brand"]:checked').value,
        car_year: document.querySelector('input[name="year"]:checked').value,
        car_model: document.querySelector('input[name="model"]:checked').value,
        car_trim: document.querySelector('input[name="trim"]:checked').value,
        car_service_type: result.serviceType.id,
        car_service_category: result.serviceType.serviceCategory.id,
        car_services: result.serviceType.serviceCategory.services,
    };
    
    localStorage.setItem('selections', JSON.stringify(selections));
}


// Booking from saved cars parse Credential in backend

function selectedBookingCredential(car_id, brand, model, year, trim, car_vno) {
    
    try {
        const locationElement = document.getElementById('location');

        const selections = {
            service_location: locationElement.value,
            car_brand: brand,
            car_year: model,
            car_model: year,
            car_trim: trim,
            car_vno: car_vno,
            car_service_type: result.serviceType.id,
            car_service_category: result.serviceType.serviceCategory.id,
            car_services: result.serviceType.serviceCategory.services,
        };
          
        
        const csrftoken = getCookie('csrftoken');
        
        
        fetch(`/booking-service/${parseInt(car_id)}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(selections)
        })
        .then(response => {
            if (!response.ok) {
                console.log('response', response);
                throw new Error(`HTTP error! status: ${response.status}`);
                
            }
            return response.json();
        })
        .then((data) => {
            const hideContent = document.getElementById('main_container');
            const newContent = `
                <div class="text-center" style="margin-top:5%">
                    <h2 class="text-primary">Booking ${data.status}!</h2>
                    <p class="lead text-muted">${data.message}</p>
                    <div class="mt-4">
                        <a href="http://127.0.0.1:8000/user/dashboard" class="btn btn-primary btn-lg">
                            <i class="bi bi-arrow-right-circle"></i> Go to Dashboard
                        </a>
                    </div>
                </div>
            `;
            hideContent.innerHTML = newContent;

        })
        .catch(error => {
            messageElement = document.getElementById('final_error')
            messageElement.parentNode.classList.remove('hidden')
            messageElement.innerHTML = error
        });

    } catch (error) {
        console.error('Error in selectedBookingCredential:', error);
        // Handle error appropriately
    }
}



// //------------------------ Saved the Quote form data ---------------------------

function submitStoredForm(user) {
    const storedFormData = JSON.parse(localStorage.getItem('selections'));
    
    if (storedFormData) {
        const formData = new FormData();
        
        const flatFields = [
            'service_location',
            'car_brand',
            'car_year',
            'car_model',
            'car_trim',
            'car_service_type',
            'car_service_category',
            'car_services'
        ];
        
        let hasErrors = false;
        flatFields.forEach(field => {
            if (storedFormData[field]) {
                formData.append(field, storedFormData[field]);
            } else {
                console.error(`Error: ${field} is required.`);
                hasErrors = true;
            }
        });
        
        if (hasErrors) {
            // Display error messages to the user
            alert('Please fill out all required fields.');
            return;
        }
        
        if (storedFormData.car_sub_services && Array.isArray(storedFormData.car_sub_services)) {
            const transformedSubServices = storedFormData.car_sub_services.map(subService => ({
                subService: subService.subService,
                title: subService.title,
                selectedOptions: subService.options.map(opt => opt.id)
            }));
            
            formData.append('car_sub_services', JSON.stringify(transformedSubServices));
        }

        // Ensure car_services data is properly stringified
        if (storedFormData.car_services) {
            formData.append('car_services', JSON.stringify(storedFormData.car_services));
        }
        
        formData.append('user', user);
        const csrftoken = getCookie('csrftoken');
    
        fetch('/user/request-a-quote', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            credentials: 'include',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'error') {
                // Display error messages to the user
                messageElement = document.getElementById('final_error')
                messageElement.parentNode.classList.remove('hidden')
                messageElement.innerHTML = data.message
            } else {
                messageElement = document.getElementById('final_error')
                messageElement.parentNode.classList.remove('hidden')
                messageElement.innerHTML = data.message
                localStorage.removeItem('selections');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            messageElement = document.getElementById('final_error')
                messageElement.innerHTML = error
        });
    } else {
        messageElement = document.getElementById('final_error')       
        // console.error('No data found in localStorage.');
    }
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function sendQuote(formId, id, service_title, description){

    const modal = document.getElementById(formId);
    const updateForm = modal.querySelector('.update-form')

    const booking_id = modal.querySelector('#booking-id')
    booking_id.innerHTML = `Booking-id:- ${id}`

    // const serviceTitle = modal.querySelector('#service_title')
    // serviceTitle.innerHTML = service_title

    const update_Service = modal.querySelector('#updateServices')
    update_Service.setAttribute('href', `http://127.0.0.1:8000/admin/service-update/${id}/`)

    var url = '/admin/booking-management/id/'.replace('id', parseInt(id));
    updateForm.setAttribute('action', url);

    
    // fetch(`http://127.0.0.1:8000//admin/booking-service-data/${id}`)
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error('Network response was not ok');
    //         }
    //         return response.json(); 
    //     })
    //     .then(data => {
    //         console.log(data);    
    //     })
    //     .catch(error => {
    //         console.error('There was an error with the fetch operation:', error);
    //     });


    // const serviceDescription = modal.querySelector('#serviceDescription')
    // serviceDescription.innerHTML += description    

    modal.style.display = 'flex';
}


function showDescription(){
    
    const service_Description = document.getElementById('serviceDescription')
    
    if (!service_Description.classList.contains("hidden")){
        service_Description.classList.add("hidden")
    } else{
        service_Description.classList.remove("hidden")
    }
}


// ------------------Calendar js------------------

function scheduleBookingPopup(formId, date) {
    const modal = document.getElementById(formId);
    const selected_date = document.getElementById('selected_date');
    selected_date.setAttribute('placeholder', date);
    selected_date.setAttribute('value', date);
    
    modal.style.display = 'flex';
}

function bookingCalendar(unavailable_dates, selected_loc) {
    
    var calendarEl = document.getElementById('calendar');
    if (!calendarEl) {
        console.warn('Error: Calendar element not found');
        return;s
    }
    
    try {
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth'
            },
            selectable: true,
            selectMirror: true,
            unselectAuto: false,
            
            // Validate date selection
            selectAllow: function(selectInfo) {
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                const selectedDate = new Date(selectInfo.startStr);
                
                // Check if date is not before today and not in disabled dates
                return selectedDate >= today && !unavailable_dates.includes(selectInfo.startStr);
            },
            
            // Handle date click
            dateClick: function(info) {
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                const selectedDate = new Date(info.dateStr);
                
                if (selectedDate >= today && !unavailable_dates.includes(info.dateStr)) {
                    scheduleBookingPopup('addForm', info.dateStr);
                    initializeMap(selected_loc);
                }
            },
            
            // Style disabled and past dates
            dayCellDidMount: function(info) {
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                
                if (info.date < today) {
                    // Past dates
                    info.el.classList.add('fc-day-past-disabled');
                } else if (unavailable_dates.includes(info.date.toISOString().split('T')[0])) {
                    // Already booked dates
                    info.el.classList.add('fc-day-booked');
                    
                    // Add tooltip container
                    const tooltipDiv = document.createElement('div');
                    tooltipDiv.classList.add('booking-tooltip');
                    tooltipDiv.textContent = 'Another booking';
                    info.el.appendChild(tooltipDiv);
                    
                    // Add event listeners for tooltip
                    info.el.addEventListener('mouseenter', function() {
                        tooltipDiv.style.display = 'block';
                    });
                    
                    info.el.addEventListener('mouseleave', function() {
                        tooltipDiv.style.display = 'none';
                    });
                }
            },
            
            // Disable past dates in month navigation
            validRange: {
                start: new Date().toISOString().split('T')[0]
            }
        });
        
        calendar.render();
        
    } catch (error) {
        console.warn('Error creating or rendering calendar:', error.message);
    }
}


// Booking schedule functions

function selectSlot(selectedSlot) {
    const timeSlots = document.querySelectorAll('.time-slot');
    timeSlots.forEach(slot => {
        slot.classList.remove('selected');
    });
    selectedSlot.classList.add('selected');
    const radio = selectedSlot.querySelector('input[type="radio"]');
    radio.checked = true;
}


function selectPaymentMethod(event) {
    event.preventDefault();
    let selectedSlot = event.target;
    
    const timeSlotSelected = document.querySelector('input[name="schedule_time_slot"]:checked');
    
    if (!timeSlotSelected) {
        alert("Please select a time slot before proceeding with payment.");
    } else{ 
    const timeSlots = document.querySelectorAll('.paymentMethod');
    timeSlots.forEach(slot => {
        slot.classList.remove('selected');
    });
    if(selectedSlot.classList.contains('remove_bottom_margin')) {
        selectedSlot = selectedSlot.parentNode;
    }
    selectedSlot.classList.add('selected');
    const radio = selectedSlot.querySelector('input[type="radio"]');
    radio.checked = true;}
}


function submitForm(event) {
    event.preventDefault();

    // Ensure that payment method is selected
    const paymentSelected = document.querySelector('input[name="payment_mode"]:checked');
    
    if (!paymentSelected) {
        isValid = false;
        alert("Please select a payment method before submitting.");
    } else{
        document.getElementById('myFrom').submit();
    }
}

// -----------------For show the map-----------------

function initializeMap(locationName = 'London') {

    // Set the default map view (centered on London)
    var map = L.map('map').setView([51.505, -0.09], 13);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Add the geocoder search control
    var geocoder = L.Control.Geocoder.nominatim();
    var control = L.Control.geocoder({
        geocoder: geocoder,
        placeholder: 'Search for a location...',
        defaultMarkGeocode: true
    }).addTo(map);

    // Handle location found after search
    control.on('markgeocode', function(e) {
        var bbox = e.geocode.bbox;
        var poly = L.polygon([
            [bbox.getSouthEast().lat, bbox.getSouthEast().lng],
            [bbox.getNorthEast().lat, bbox.getNorthEast().lng],
            [bbox.getNorthWest().lat, bbox.getNorthWest().lng],
            [bbox.getSouthWest().lat, bbox.getSouthWest().lng]
        ]).addTo(map);

        // Adjust the map view to fit the selected bounds
        map.fitBounds(poly.getBounds());
    });

    // If a location name is passed, geocode that location and center the map on it
    if (locationName) {
        geocoder.geocode(locationName, function(results) {
            if (results && results.length > 0) {
                var latLng = results[0].center; // Get the coordinates of the first result

                // Set the map view to the geocoded location
                map.setView(latLng, 13);

                // Add a marker at the location
                L.marker(latLng).addTo(map)
                    .bindPopup(locationName)
                    .openPopup();
            } else {
                alert("Location not found!");
            }
        });
    }

    // Show current location if available
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            // Get the latitude and longitude
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;

            // Set the map view to the current location
            map.setView([lat, lng], 13);

            // Add a marker at the current location
            L.marker([lat, lng]).addTo(map)
                .bindPopup("You are here")
                .openPopup();
        }, function(error) {
            alert("Geolocation failed: " + error.message);
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}



// Total sum of Quote 
function updatePrice(elm1, elm2, elm3){
    const p1 = document.getElementById(elm1).value
    const p2 = document.getElementById(elm2).value
    const p3 = document.getElementById(elm3)
    
    let total = parseFloat(p1)+parseFloat(p2)
    p3.setAttribute('value', parseFloat(total))
}


// Used for show assign mechanic pop up and update value into that
function assignMechanic(formId, id, scheduleDate, user){
    
    const modal = document.getElementById(formId);

    const assignForm = modal.querySelector('.assign-form')
    
    var url = '/admin/booking-management/id/'.replace('id', parseInt(id));
    assignForm.setAttribute('action', url);

    const bookingId = modal.querySelector('#specific-booking-id')
    bookingId.innerHTML = `(Booking Id : ${id})`;

    const detailsPara =  modal.querySelector('#details-para');
    detailsPara.innerHTML = `<strong>${user}</strong> user wants a booking to be 
                            scheduled on date <strong>${scheduleDate}</strong>`;
                            
    const dateInput = modal.querySelector('#date-Input');
    dateInput.value = scheduleDate; 


    fetch(`http://127.0.0.1:8000/admin/mechanic-data/?date=${scheduleDate}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); 
        })
        .then(data => {      
            const mechanicSelect = document.getElementById('mechanic-selction');
        
            // Clear previous options (optional, if you want to reset the list)
            mechanicSelect.innerHTML = '<option value="">Select Mechanic: </option>';

            // Loop through the data and create <option> elements
            data.forEach(mechanic => {
                const option = document.createElement('option');
                option.value = mechanic.user_id; // Set the value to user_id
                option.textContent = `${mechanic.first_name} ${mechanic.last_name}`; // Display the full name
                mechanicSelect.appendChild(option); // Append the option to the select
            });    
        })
        .catch(error => {
            console.error('There was an error with the fetch operation:', error);
        });


    modal.style.display = 'flex';
}


function updateStatusModal(formId, bookingId, bookingStatus) {
    const modal = document.getElementById(formId);
    const Form = modal.querySelector('#update_form')

    const showBookingId = modal.querySelector('#showBookingId')
    showBookingId.innerHTML = `Booking Id - ${bookingId}`

    const booking_Status = modal.querySelector('#bookingStatus')
    booking_Status.innerHTML = `Current Status - ${bookingStatus}`

    var url = '/admin/Update-booking-management/id/'.replace('id', parseInt(bookingId));
    Form.setAttribute('action', url);

    modal.style.display = 'flex';
}


function carDetails(formId, bookingId, vno, status){
    const modal = document.getElementById(formId);

    const Form = modal.querySelector('#car_detail_form')
    var url = '/admin/Update-booking-management/id/'.replace('id', parseInt(bookingId));
    Form.setAttribute('action', url);

    const carVno = modal.querySelector('#car_vno')
    carVno.setAttribute('value', vno)

    const bookingStatus = modal.querySelector('#booking_status')
    bookingStatus.setAttribute('value', status)
    
    modal.style.display = 'flex';
}


//--------------------Used for Car History --------------------

function userCarHistory(formId, carId, userId) {
    const modal = document.getElementById(formId);
    const historyFormContainer = document.querySelector('.history-form');
    const spinner = document.querySelector('.spinner');

    // Show the spinner
    spinner.style.display = 'block';

    fetch(`/car-service-history/?car_id=${carId}&user_id=${userId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            let htmlContent = '';

            // Process each service in the data array
            data.forEach(service => {
                const serviceList = service.car_services.map(serviceTitle => `<li>${serviceTitle}</li>`).join('');

                // Build the HTML content for each service
                htmlContent += `
                    <div class="col-sm-12 col-md-12 py-2 historyItem">
                        <div class="panel panel-info lobidisable">
                            <div class="panel-heading">
                                <div class="panel-title">
                                    <h4 style="background:#6481c252;">Service Date: ${service.schedule_at || 'N/A'}</h4>
                                </div>
                            </div>
                            <div class="panel-body">
                                <div class="row">
                                    <div class="col-md-12 col-sm-12">
                                        <h4>Services</h4>
                                        <ul>
                                            ${serviceList || '<li>N/A</li>'}
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer">
                                <div class="row m-0" style="background:#6481c252;">
                                    <div class="col-sm-12 col-md-4 p-1" style="max-width:25%;">
                                        <strong>Location: </strong>${service.service_location || 'N/A'}
                                    </div>
                                    <div class="col-sm-12 col-md-4 p-1" style="max-width:25%;">
                                        <strong>Price: </strong>${service.total_service_amount || 'N/A'}
                                    </div>
                                    <div class="col-sm-12 col-md-4 p-1" style="max-width:25%;">
                                        <strong>Mechanic: </strong>${service.mechanic || 'N/A'}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <hr class="someClass" style="background:#6481c252;">
                `;
            });

            // Display the history content in the modal
            historyFormContainer.innerHTML = htmlContent;

            // Hide the spinner
            spinner.style.display = 'none';
        })
        .catch(error => {
            console.error('There was an error with the fetch operation:', error);
            // Hide the spinner in case of error
            spinner.style.display = 'none';
        });

    // Show the modal
    modal.style.display = 'flex';
}



// Used for get the Combo management page

function getServiceCategory(servicetype, servicecategory) {
    const serviceType = document.getElementById(servicetype).value;
    fetch(`/get-service-category/?service_type=${serviceType}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); 
        })
        .then(data => {
            let htmlcontent = '<option value="">Select Category type here</option>'; 
            const target_element = document.getElementById(servicecategory);
           
            for (let i = 0; i < data.length; i++) {
                htmlcontent += `<option value="${data[i].id}">${data[i].service_category_name}</option>`;
            }

            target_element.innerHTML = htmlcontent;
        })
        .catch(error => {
            console.error('There was an error with the fetch operation:', error);
        });
}

// Function to get services based on service category
function getService(servicecategory, service, service_selection) {
    const service_cat = document.getElementById(servicecategory).value;
    
    fetch(`/get-services/?service_category=${service_cat}`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            let htmlContent = '<label class="w-25" for="service_type">Service</label>';
            const target_element = document.getElementById(service);
            
            data.forEach(item => {
                htmlContent += `
                    <div id="option-${item.id}"
                        class="service-item"
                        onclick="selectService('${item.id}', '${item.service_title}')">
                        <p class="m-0">${item.service_title}</p>
                    </div>`;
            });
            
            target_element.innerHTML = htmlContent;
            document.getElementById('subServiceOption').innerHTML = '';
        })
        .catch(error => {
            console.error('Error fetching services:', error);
        });
}

// Function to select a service
function selectService(serviceId, serviceTitle) {
    // Clear previous selection
    document.querySelectorAll('.service-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    // Update current selection
    const serviceElement = document.getElementById(`option-${serviceId}`);
    if (serviceElement) {
        serviceElement.classList.add('selected');
    }
    
    currentServiceId = serviceId;
    showSubServiceOptions(serviceId, serviceTitle);
}

// Function to show sub-service options
function showSubServiceOptions(serviceId, serviceTitle) {
    const target_element = document.getElementById('subServiceOption');
    
    fetch(`/get-sub-service/?service=${serviceId}`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(subServices => {
            const processSubService = async (subService) => {
                const response = await fetch(`/get-sub-service-option/?sub_service=${subService.id}`);
                const options = await response.json();
                
                return `
                    <div class="sub-service-container" data-service-id="${serviceId}">
                        <div class="question-container">
                            <div class="question-title">
                                <h6 class="m-0">${subService.title}</h6>
                            </div>
                            <div class="options-container" id="options-${subService.id}"
                                data-sub-service-id="${subService.id}"
                                data-sub-service-title="${subService.title}">
                                ${createOptionsHTML(subService, options)}
                            </div>
                        </div>
                    </div>`;
            };
            
            Promise.all(subServices.map(processSubService))
                .then(htmlContents => {
                    const addButtonHTML = `
                        <div class="text-center mt-3">
                            <button type="button" class="action-button add-button"
                                    onclick="addToSelected('${serviceId}', '${serviceTitle}')">
                                Add Service
                            </button>
                        </div>`;
                    
                    target_element.innerHTML = htmlContents.join('') + addButtonHTML;
                });
        })
        .catch(error => {
            console.error('Error:', error);
            target_element.innerHTML = 'Error loading options. Please try again.';
        });
}

// Function to create options HTML
function createOptionsHTML(subService, options) {
    const inputType = subService.selection_type === 'Multiple' ? 'checkbox' : 'radio';
    
    return options.map(option => `
        <div class="option-item">
            <input type="${inputType}" 
                id="option-${subService.id}-${option.id}" 
                name="subService-${subService.id}" 
                value="${option.id}"
                data-option-title="${option.title}"
                onchange="handleOptionChange('${subService.id}', '${option.id}', '${option.title}')"
                class="form-check-input me-2">
            <label for="option-${subService.id}-${option.id}" class="form-check-label">
                ${option.title}
            </label>
        </div>
    `).join('');
}

// Function to handle option change
function handleOptionChange(subServiceId, optionId, optionTitle) {
    const input = document.getElementById(`option-${subServiceId}-${optionId}`);
    const optionContainer = input.closest('.option-item');
    
    if (input.type === 'radio') {
        const groupOptions = document.getElementsByName(`subService-${subServiceId}`);
        groupOptions.forEach(opt => {
            opt.closest('.option-item').classList.remove('selected');
        });
    }
    
    if (input.checked) {
        optionContainer.classList.add('selected');
    } else {
        optionContainer.classList.remove('selected');
    }
}

// Function to add selected service to the list
function addToSelected(serviceId, serviceTitle) {
    // Retrieve existing selected services from local storage
    selectedServices = JSON.parse(localStorage.getItem('selectedServices')) || {};
    
    const serviceType = document.getElementById('service_type').value;
    const serviceCategoryId = document.getElementById('service_category').value;
    const subServiceContainers = document.querySelectorAll(`[data-service-id="${serviceId}"] .options-container`);
    
    // Create the service object with the correct structure
    const serviceData = {
        serviceId: serviceId,
        serviceType: serviceType,
        service_title: serviceTitle,
        service_category_id: serviceCategoryId,
        sub_services: []
    };

    // Process each sub-service container
    subServiceContainers.forEach(container => {
        const subServiceId = container.dataset.subServiceId;
        const subServiceTitle = container.dataset.subServiceTitle;
        const selectedInputs = container.querySelectorAll('input:checked');
        
        // Create sub-service object even if no options are selected
        const subServiceData = {
            sub_service_id: subServiceId,
            sub_service_title: subServiceTitle,
            sub_service_options: []
        };

        // Add selected options if any
        selectedInputs.forEach(input => {
            subServiceData.sub_service_options.push({
                sub_service_option_id: input.value,
                sub_service_option_title: input.dataset.optionTitle
            });
        });

        serviceData.sub_services.push(subServiceData);
    });
    
    selectedServices[serviceId] = serviceData; // Add or update the service in selectedServices
    localStorage.setItem('selectedServices', JSON.stringify(selectedServices)); // Save to local storage
    updateSelectedServicesDisplay(selectedServices); // Update display
    testItem = localStorage.getItem('selectedServices', JSON.stringify(selectedServices));
    

    // Clear current selection
    currentServiceId = null;
    document.querySelectorAll('.service-item').forEach(item => {
        item.classList.remove('selected');
    });
    document.getElementById('subServiceOption').innerHTML = '';
}

// Function to update selected services display
function updateSelectedServicesDisplay(services) {
    
    const container = document.getElementById('selected_services_container');
    let html = '';
    
    for (const [serviceId, serviceData] of Object.entries(services)) {
        html += `
            <div class="selected-service" id="selected-${serviceId}">
                <div class="d-flex justify-content-between align-items-center">
                    <strong>${serviceData.service_title}</strong>
                    <button type="button" class="action-button remove-button" 
                            onclick="removeFromSelected('${serviceId}')">
                        Remove
                    </button>
                </div>`;
        
        // Add selected options
        serviceData.sub_services.forEach(subService => {
            if (subService.sub_service_options.length > 0) {
                html += `
                    <div class="selected-options">
                        <div class="sub-service-title">${subService.sub_service_title}</div>`;
                
                subService.sub_service_options.forEach(option => {
                    html += `<div class="selected-option">• ${option.sub_service_option_title}</div>`;
                });
                
                html += `</div>`;
            }
        });
        
        html += `</div>`;
    }
    
    container.innerHTML = html;
}

// Function to remove a service from selected services
function removeFromSelected(serviceId) {
    // Retrieve existing selected services from local storage
    selectedServices = JSON.parse(localStorage.getItem('selectedServices')) || {};
    delete selectedServices[serviceId];
    localStorage.setItem('selectedServices', JSON.stringify(selectedServices));
    
    // Update display
    updateSelectedServicesDisplay(selectedServices);
    
    // Clear sub-service options if the removed service was currently selected
    if (currentServiceId === serviceId) {
        currentServiceId = null;
        document.getElementById('subServiceOption').innerHTML = '';
    }
}

// Function to reset the entire selection
function resetSelection() {
    localStorage.removeItem('selectedServices');
    selectedServices = {};
    
    // Clear display
    document.getElementById('selected_services_container').innerHTML = '';
    
    // Reset form elements
    document.getElementById('service_type').selectedIndex = 0;
    document.getElementById('service_category').innerHTML = '<option value="">Select Category type here</option>';
    document.getElementById('service').innerHTML = '';
    document.getElementById('subServiceOption').innerHTML = '';
    
    // Reset current service
    currentServiceId = null;
}


function updateLocalStorage() {
try {
    const csrftoken = getCookie('csrftoken');
    comboName = document.getElementById('combo_name').value
    price = document.getElementById('price').value
    discountPrice = document.getElementById('discount_price').value
    start_date = document.getElementById('start_date').value
    end_date = document.getElementById('end_date').value
    usage_limit = document.getElementById('usage_limit').value
    
    // Format the data for the backend
    const backendData = {
        services: Object.values(selectedServices)
    };
    backendData["price"] = price
    backendData["end_date"] = end_date
    backendData["comboName"] = comboName
    backendData["start_date"] = start_date
    backendData["discountPrice"] = discountPrice
    backendData["usage_limit"] = usage_limit
    
    fetch(`/admin/combo-management/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(backendData)
    })
    .then(response => {
        console.log('response', response);
        
        if (!response.ok) {
            return response.text().then(text => {
                console.error(`Network response was not ok: ${text}`);
                throw new Error(`Network response was not ok: ${text}`);
            });
        }
        return response.json();
    })  
    .then(data => {
        console.log('data', data);
        if (data.status === 'success') {
            alert(data.messages);
            redirectToNotification('http://127.0.0.1:8000/admin/combo-management/')
        } else {
            alert(data.message || 'Update failed');
        }
    })
    .catch(error => {
        console.log('Error:', error);
        // alert(`Failed to update services. Please try again.`);   
    });
} catch (error) {
    console.error('Error:', error);
    alert('An unexpected error occurred');
}
}


function combo_detail(formId, id, is_combo_selection, user_combo_id) {
    const container = document.getElementById('combo-details-container');
    container.innerHTML = '';

    
    fetch(`/combo/operation/${id}`)

        .then(response => response.json())
        .then(data => {            
            addopenModal(formId)
            
            if (is_combo_selection){
                renderComboD(data.services, user_combo_id)
            } else{
                renderComboDetails(data.services);
            }
        })
        .catch(error => console.error('Error fetching combo details:', error));
}


function renderComboDetails(services) {
    const container = document.getElementById('combo-details-container');
    container.innerHTML = '';

    services.forEach(service => {
        const serviceElement = document.createElement('div');
        serviceElement.classList.add('combo-item');

        serviceElement.innerHTML = `
            <h3>${service.service_title}</h3>
            <p><strong>Service Type:</strong> ${service.service_type_name}</p>
            <p><strong>Service Category:</strong> ${service.service_category_name}</p>
            <h4>${service.sub_service_title}</h4>
            <ul>
                ${service.sub_service_option_id
                    .map(option => `<li>${option.title}</li>`)
                    .join('')}
            </ul>   
        `;
        container.appendChild(serviceElement);
    });
}


// Used to show the Combo data to user's

function renderComboD(services, user_combo_id) {
    const container = document.getElementById('combo-details-container');
    
    const existingServicesMap = new Map();
    services.forEach(service => {
        const serviceKey = `${service.service}-${service.service_type}`;

        if (existingServicesMap.has(serviceKey)) {
            const existingServiceElement = existingServicesMap.get(serviceKey);
            
            const existingOptionsContainer = existingServiceElement.querySelector('.options-container');
            const optionsHTML = service.sub_service_option_id
                .map((option, index) => 
                    `<div data-value="${option.id}" class="option">
                        ${index + 1}. ${option.title}
                    </div>`
                )
                .join('');
            
            existingOptionsContainer.innerHTML += `
                <p class="sub_service" data-value="${service.sub_service_id}" class="my-0">
                    Sub Service Question:- ${service.sub_service_title}
                </p>
                ${optionsHTML}
            `;
        } else {
            const serviceElement = document.createElement('div');
            serviceElement.classList.add('combo-item');
            serviceElement.classList.add('clickable-service');

            const optionsHTML = service.sub_service_option_id
                .map((option, index) => 
                    `<div data-value="${option.id}" class="option">
                        ${index + 1}. ${option.title}
                    </div>`
                )
                .join('');

            serviceElement.innerHTML = `
                <div class="service-header">
                    <input value="${user_combo_id}" id="combo_id" name="combo_id" hidden>
                    <h3 id="service" data-value="${service.service}">${service.service_title}</h3>
                    <p id="service_type" data-value="${service.service_type}" class="my-0">
                        Service Type:- ${service.service_type_name}
                    </p>
                    <p id="service_category" data-value="${service.service_category}" class="my-0">
                        Service Category:- ${service.service_category_name}
                    </p>
                    <p class="sub_service" data-value="${service.sub_service_id}" class="my-0">
                        Sub Service Question:- ${service.sub_service_title}
                    </p>
                </div>
                <div class="options-container">
                    ${optionsHTML}
                </div>
            `;

            serviceElement.addEventListener('click', function() {
                const isSelected = serviceElement.classList.toggle('selected');
            });

            container.appendChild(serviceElement);
            existingServicesMap.set(serviceKey, serviceElement);
        }
    });
}


function collectSelectedOptions(test){
    const testelement= document.getElementById(test)
    const backendFinalData = [];
    testelement.childNodes.forEach(el => {
    const backendData = {};
        if (el.classList.contains('selected')){
            const serviceHeader = el.querySelector('.service-header')
            const optionsContainer = el.querySelector('.options-container')
            let sub_services = ''
            console.log('sub_service', document.querySelectorAll('.sub_service'));            
            document.querySelectorAll('.sub_service').forEach(sub_service => {
                sub_services += sub_service.getAttribute('data-value') + ','
                console.log('sub_servicesss', sub_services);
                
            })
            
            let options = ''
            optionsContainer.querySelectorAll('.option').forEach(option =>{
                options += option.getAttribute('data-value') + ','
            });
            
            const service = serviceHeader.querySelector('#service').getAttribute('data-value')
            const service_type = serviceHeader.querySelector('#service_type').getAttribute('data-value')
            const service_category = serviceHeader.querySelector('#service_category').getAttribute('data-value')
            const combo_id = serviceHeader.querySelector('#combo_id').value
            const location = document.getElementById('service_location').value
            
            backendData["service"] = service
            backendData["service_type"] = service_type
            backendData["service_category"] = service_category
            backendData["sub_service"] = sub_services
            backendData["sub_service_options"] = options
            backendData["combo_id"] = combo_id
            backendData["location"] = location
        }
        backendFinalData.push(backendData)
        
    })
    
    let csrftoken = getCookie('csrftoken');
    fetch(`/combo/booking/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(backendFinalData)
    })
    .then(response => {
        
        if (!response.ok) {
            return response.text().then(text => {
                console.error(`Network response was not ok: ${text}`);
                throw new Error(`Network response was not ok: ${text}`);
            });
        }
        return response.json();
    })  
    .then(data => {
        if (data.status === 'success') {
            alert(data.messages);
            redirectToNotification('http://127.0.0.1:8000/admin/combo-management/')
        } else {
            alert(data.message || 'Update failed');
        }
    })
    .catch(error => {
        console.log('Error:', error);
        // alert(`Failed to update services. Please try again.`);   
    });
    
}




// function combo_car_selection(formId, id){
//     const modal = document.getElementById(formId);

//     const Form = modal.querySelector('#car_selection')
//     var url = `http://127.0.0.1:8000/combo/operation/${id}`;
//     Form.setAttribute('action', url);

//     modal.style.display = 'flex';
// }