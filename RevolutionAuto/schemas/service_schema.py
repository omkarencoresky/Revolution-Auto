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
            "description": "Service Type Name must be have 3-50 characters and allowed only alphabets."
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
            "description": "Service Category Name must be have 3-50 characters and allowed only alphabets."
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
            "description": "Service title Name must be have 3-50 characters and allowed only alphabets."
            },
        "service_description": {
            "type": "string",
            "minLength": 4,
            "maxLength": 1000,
            "pattern": "^[a-zA-Z0-9& ]+$",
            "description": "Service description must have atleast 4 characters and allowed only alphabets and numbers."
            },
    },
    "required": ["service_description", "service_category", 'service_title'],
    "additionalProperties": True
}

validate_services_details = fastjsonschema.compile(services_schema)
validate_service_type_details = fastjsonschema.compile(service_type_schema)
validate_service_category_details = fastjsonschema.compile(service_category_schema)