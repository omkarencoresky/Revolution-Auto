import fastjsonschema
import fastjsonschema

# Define the schema for Service_Type
service_type_schema = {
    "type": "object",
    "properties": {
        "service_type_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z& ]+$",
            "description": "Service Type Name should be have 3-50 characters and allowed only alphabets."
            },
    },
    "required": ["service_type_name"],
    "additionalProperties": True
}


# Define the schema for Service_Category
service_category_schema = {
    "type": "object",
    "properties": {
        "service_type": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a service type."
            },
        "service_category_name": {
            "type": "string",
            "minLength": 4,
            "maxLength": 150,
            "pattern": "^[a-zA-Z& ]+$",
            "description": "Service Category Name should be have 3-50 characters and allowed only alphabets."
            },
    },
    "required": ["service_type", "service_category_name"],
    "additionalProperties": True
}



# Define the schema for Service_Category
services_schema = {
    "type": "object",
    "properties": {
        "service_category": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a service category."
            },
        "service_title": {
            "type": "string",
            "minLength": 4,
            "maxLength": 150,
            "pattern": "^[a-zA-Z& ]+$",
            "description": "Service title Name should be have 3-50 characters and allowed only alphabets."
            },
        # "description": {
        #     "type": "string",
        #     "minLength": 3,
        #     "maxLength": 2000,
        #     "pattern": "^(?!\\s*$).+",
        #     "description": "Description should have at-least 3 characters and not allowed blank."
        #     }

    },
    "required": [ "service_category", 'service_title'],
    "additionalProperties": True
}

# Define the schema for sub_services
sub_services_schema = {
    "type": "object",
    "properties": {
        "service": {
            "type": "string",
            "pattern": "^\\d+$",
            "description": "Please select a service category."
        },
       "display_text": {
            "type": "string",
            "minLength": 4,
            "maxLength": 150,
            "pattern":  "^[a-zA-Z @~`!@#%^&*()_=+\\\\';:\\\"/?>.<,-]*$",
            "description": "Display text should contains at least 4 characters and not allowed the blanks."
        },
        "title": {
            "type": "string",
            "minLength": 4,
            "maxLength": 150,
            "pattern": "^.+$",
            "description": "Sub Service title should contains at least 4 characters and not allowed the blanks."
        },
        # "description": {
        #     "type": "string",
        #     "minLength": 3,
        #     "maxLength": 2000,
        #     "pattern": "^(?!\\s*$).+",
        #     "description": "Description should have at-least 3 characters and not allowed blank."
        #     },        
        "order": {
            "type": "string",
            "minLength": 1,
            "maxLength": 999,
            "pattern": "^\\d+$",
            "description": "Order allows only numbers."
        },
        "optional": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10,
            "pattern": "^.*$",
            "description": "Optional cannot be left blank."
        },
        "selection_type": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10,
            "pattern": "^.*$",
            "description": "Selection Type cannot be left blank."
        },
        "status": {
            "type": "integer",
            "minLength": 1,
            "maxLength": 2,
            "pattern": "^.*$",
            "description": "status Type cannot be left blank."
        },
    },
    "required": ["service", "title", "order"],
    "additionalProperties": True
}


# Define the schema for sub_services_option
sub_services_option_schema = {
    "type": "object",
    "properties": {
        "sub_service": {
            "type": "string",
            "pattern": "^\\d+$",
            "description": "Please select a sub-service category."
        },
        "option_type": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50,
            "pattern": "^[a-zA-Z ]*$",
            "description": "Option type cannot be left blank."
        },
        "title": {
            "type": "string",
            "minLength": 4,
            "maxLength": 150,
            "pattern": "^.+$",
            "description": "Option title should contains at least 4 characters and not allowed the blanks."
        },
        # "description": {
        #     "type": "string",
        #     "minLength": 3,
        #     "maxLength": 2000,
        #     "pattern": "^(?!\\s*$).+",
        #     "description": "Description should have at-least 3 characters and not allowed blank."
        #     },
        "order": {
            "type": "string",
            "minLength": 1,
            "maxLength": 999,
            "pattern": "^\\d+$",
            "description": "Order allows only numbers and cannot be left blank."
        },
        "option_image":{
            "type": "string",
            "minLength": 0,
            "maxLength": 10,
            "pattern": "^(?:$|.*\.?(jpg|jpeg|png|gif))$",
            "description": "In-valid image format, try agin with different image format."
        }
    },
    "required": ["sub_service", "title", "option_type", "order" ],
    "additionalProperties": True
}


validate_services_details = fastjsonschema.compile(services_schema)
validate_sub_service_details = fastjsonschema.compile(sub_services_schema)
validate_service_type_details = fastjsonschema.compile(service_type_schema)
validate_service_category_details = fastjsonschema.compile(service_category_schema)
validate_sub_service_option_details = fastjsonschema.compile(sub_services_option_schema)
