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
        "service_description": {
            "type": "string",
            "minLength": 4,
            "maxLength": 1000,
            "pattern": "^[a-zA-Z0-9& ]+$",
            "description": "Service description should have atleast 4 characters and allowed only alphabets and numbers."
            },
    },
    "required": ["service_description", "service_category", 'service_title'],
    "additionalProperties": True
}


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
            # "pattern":  "^[A-Z@~`!@#$%^&*()_=+\\\\';:\\\"/?>.<,-]*$",
            "description": "Display text should have at least 4 characters and not allowed the blanks."
        },
        "sub_service_title": {
            "type": "string",
            "minLength": 4,
            "maxLength": 150,
            "pattern": "^.+$",
            "description": "Service title should have at least 4 characters and not allowed the blanks."
        },
        "sub_service_description": {
            "type": "string",
            "minLength": 4,
            "maxLength": 1000,
            # "pattern": "^[a-zA-Z!@#$%^&*?/]*$",
            "description": "Service description should have at least 4 characters and not allowed numbers."
        },
        "order": {
            "type": "string",
            "minLength": 1,
            "maxLength": 999,
            "pattern": "^\\d+$",
            "description": "Order only allowed numbers."
        }
    },
    "required": ["service", "sub_service_title", "sub_service_description", "order"],
    "additionalProperties": True
}



validate_services_details = fastjsonschema.compile(services_schema)
validate_service_type_details = fastjsonschema.compile(service_type_schema)
validate_service_category_details = fastjsonschema.compile(service_category_schema)
validate_sub_service_details = fastjsonschema.compile(sub_services_schema)
