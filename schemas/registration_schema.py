import fastjsonschema

# User credential validation for registration
registration_schema = {
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z ]+$",  # Only alphabets
            "description": "First name should be 3 to 50 characters long and contain only alphabets."
        },
        "last_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z ]+$",  # Only alphabets
            "description": "Last name should be 3 to 50 characters long and contain only alphabets."
        },
        "email": {
            "type": "string",
            "minLength": 10,
            "maxLength": 50,    
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",  # Standard email pattern
            "description": "Email should be between 10 to 50 characters and in a valid format."
        },
        "phone_no": {
            "type": "string",
            "minLength": 10,
            "maxLength": 10,
            "pattern": "^[0-9]+$" , # Only numbers
            "description": "Contact number contains 10 digits, allow only number's."
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLength": 20,
            "pattern":  "[A-Za-z\d!@#%^&*()_+\-=\[\]{};':\\|,.<>/?]",
            "description": "Password should be 8 to 20 characters long, with at least 1 uppercase letter and 1 special character."
        },
        "profile_image_extension":{
            "type":"string",
            "pattern": "^(jpg|jpeg|png|gif|bmp|tiff)$",
            "description": "Please select a image and with valid format like 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'."
        }
    },
    "required": ["first_name", "last_name", "email", "phone_no", "password", "profile_image_extension"],
    "additionalProperties": True
}



# user credntial validation for update 
update_detail_schema = {
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z ]+$",  # Only alphabets
            "description": "First name should be 3 to 50 characters long and contain only alphabets."
        },
        "last_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z ]+$",  # Only alphabets
            "description": "Last name should be 3 to 50 characters long and contain only alphabets."
        },
        "email": {
            "type": "string",
            "minLength": 10,
            "maxLength": 50,    
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",  # Standard email pattern
            "description": "Email should be between 10 to 50 characters and in a valid format."
        },
        "phone_no": {
            "type": "string",
            "minLength": 10,
            "maxLength": 10,
            "pattern": "^[0-9]+$" , # Only numbers
            "description": "Contact number contains 10 digits, allow only number's."
        },
        "profile_image_extension":{
            "type":"string",
            "pattern": "^(jpg|jpeg|png|gif|bmp|tiff)$",
            "description": "Please select a image and with valid format like 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'."
        }
    },
    "required": ["first_name", "last_name", "email", "phone_no"],
    "additionalProperties": True
}


# mechanic credntial validation for register
mechanic_register_schema = {
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z ]+$",  # Only alphabets
            "description": "First name should be 3 to 50 characters long and contain only alphabets."
        },
        "last_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z ]+$",  # Only alphabets
            "description": "Last name should be 3 to 50 characters long and contain only alphabets."
        },
        "email": {
            "type": "string",
            "minLength": 10,
            "maxLength": 50,    
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",  # Standard email pattern
            "description": "Email should be between 10 to 50 characters and in a valid format."
        },
        "phone_no": {
            "type": "string",
            "minLength": 10,
            "maxLength": 10,
            "pattern": "^[0-9]+$" , # Only numbers
            "description": "Contact number contains 10 digits, allow only number's."
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLength": 20,
            "pattern":  "[A-Za-z\d!@#%^&*()_+\-=\[\]{};':\\|,.<>/?]",
            "description": "Password should be 8 to 20 characters long, with at least 1 uppercase letter and 1 special character."
        },
        "profile_image_extension":{
            "type":"string",
            "pattern": "^(jpg|jpeg|png|gif|bmp|tiff)$",
            "description": "Please select a image and with valid format like 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'."
        }
    },
    "required": ["first_name", "last_name", "email", "phone_no", "password", "profile_image_extension"],
    "additionalProperties": True
}


# mechanic credntial validation for update 
mechanic_update_schema = {
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z ]+$",  # Only alphabets
            "description": "First name should be 3 to 50 characters long and contain only alphabets."
        },
        "last_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z ]+$",  # Only alphabets
            "description": "Last name should be 3 to 50 characters long and contain only alphabets."
        },
        "email": {
            "type": "string",
            "minLength": 10,
            "maxLength": 50,    
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",  # Standard email pattern
            "description": "Email should be between 10 to 50 characters and in a valid format."
        },
        "phone_no": {
            "type": "string",
            "minLength": 10,
            "maxLength": 10,
            "pattern": "^[0-9]+$" , # Only numbers
            "description": "Contact number contains 10 digits, allow only number's."
        },
        "profile_image_extension":{
            "type":"string",
            "pattern": "^(jpg|jpeg|png|gif|bmp|tiff)$",
            "description": "Please select a image and with valid format like 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'."
        }
    },
    "required": ["first_name", "last_name", "email", "phone_no"],
    "additionalProperties": True
}

validate_registration = fastjsonschema.compile(registration_schema)     
validate_update_profile_details_schema = fastjsonschema.compile(update_detail_schema)  
validate_mechanic_update_detail_schema = fastjsonschema.compile(mechanic_update_schema)
validate_mechanic_register_detail_schema = fastjsonschema.compile(mechanic_register_schema)