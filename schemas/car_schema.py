import fastjsonschema

# Define the schema for Brands
car_brand_schema = {
    "type": "object",
    "properties": {
        "brand": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z ]+$",
            "description": "Car brand should be 3 to 50 characters and allowed only alphabets."
            },
        # "description": {
        #     "type": "string",
        #     "maxLength": 50,
        #     "pattern": "^[a-zA-Z0-9 ]+$",
        #     "description": "Car description should be 3 to 50 characters and in a valid format."
        #     },
        "image_format": {
            "type": "string",
            "pattern": "^(jpg|jpeg|png|gif|bmp|tiff)*$",
            "description": "Please select a image and with valid format like 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'."
        },
    },
    "required": ["brand"],
    "additionalProperties": True
}




# Define the schema for years
car_year_schema = {
    "type": "object",
    "properties": {
        "car_id": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a car brand."
            },
        "year": {
            "type": "string",
            "minLength": 4,
            "maxLength": 4,
            "pattern": "^[0-9]{4}$",
            "description": "Car year only allowed the 4 digits."
            },
    },
    "required": ["car_id", "year"],
    "additionalProperties": True
}


# Define the schema for models
car_model_schema = {
    "type": "object",
    "properties": {
        "car_id": {
            "type": "string",
            "pattern": "^\d+$",
            "description":"Please select a car brand."
            },
        "year_id": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a car year."
            },
        "model_name": {
            "type": "string",
            "minLength": 2,
            "maxLength": 50,
            "pattern": "^[a-zA-Z0-9 ]*$",
            "description": "Car model name length between 2-50 characters and special character mot allowed."
            },
    },
    "required": ["car_id", "year_id", "model_name"],
    "additionalProperties": True
}


# Define the schema for trims
car_trim_schema = {
    "type": "object",
    "properties": {
        "car_id": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a car brand."
            },
        "year_id": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a car year."
            },
        "model_id": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a car model."
            },
        "car_trim_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z0-9. ]+$",
            "description": "Car Trim name length between 3 to 50 and special character not allowed."
            },
    },
    "required": ["car_id", "year_id", "model_id", "car_trim_name"],
    "additionalProperties": True
}


# Define the schema for add car details for user
users_car_detail_schema = {
    "type": "object",
    "properties": {
        "car_brand": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a car Brand."
            },
        "car_year": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a car Year."
            },
        "car_model": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a car Model."
            },
        "car_trim": {
            "type": "string",
            "pattern": "^\d+$",
            "description": "Please select a car Trim."
            },
        "vin_number": {
            "type": "string",
            "pattern": "^($|[a-zA-Z0-9 ]{16})$",
            "description": "VIN number length must have 16 digits and it allows only alphanumeric."
            },
    },
    "required": ["car_brand", "car_year", "car_model", "car_trim"],
    "additionalProperties": True
}

# Compile the schemas
validate_car_year_details = fastjsonschema.compile(car_year_schema)
validate_car_trim_details = fastjsonschema.compile(car_trim_schema)
validate_car_brand_details = fastjsonschema.compile(car_brand_schema)
validate_car_model_details = fastjsonschema.compile(car_model_schema)
validate_users_car_details = fastjsonschema.compile(users_car_detail_schema)