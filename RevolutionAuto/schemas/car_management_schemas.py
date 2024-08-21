import fastjsonschema

# Define the schema for Brands
car_brand_schema = {
    "type": "object",
    "properties": {
        "brand": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z]+$",
            "description": "Car brand must be 3 to 50 characters and allow only alphabets."
            },
        "description": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z0-9]+$",
            "description": "Car description must be 3 to 50 characters and in a valid format."
            },
        "image_format": {
            "type": "string",
            "pattern": "^(jpg|jpeg|png|gif|bmp|tiff)$",
            "description": "Please select atleast a image and with valid format like 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'."
        },
    },
    "required": ["brand", "description"],
    "additionalProperties": True
}

# Define the schema for years
car_year_schema = {
    "type": "object",
    "properties": {
        "car_id": {
            "type": "integer",
            "minLength": 1,
            "maxLength": 50,
            "pattern": "^\d+$",
            "description": "Car car_id length at least between 1 to 50 and only allow the numbers."
            },
        "year": {
            "type": "integer",
            "minLength": 4,
            "maxLength": 4,
            "pattern": "^\d+$",
            "description": "Car year length must be 4 and only allow the numbers."
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
            "type": "integer",
            "minLength": 1,
            "maxLength": 50,
            "pattern": "^\d+$",
            "description": "Car car_id length at least between 1 to 50 and only allow the numbers."
            },
        "year_id": {
            "type": "integer",
            "minLength": 1,
            "maxLength": 50,
            "pattern": "^\d+$",
            "description": "Car year length at least between 1 to 50 and only allow the numbers."
            },
        "model_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z0-9]*$",
            "description": "Car model name must be 3 to 50 characters."
            },
    },
    "required": ["car_id", "year", "model_name"],
    "additionalProperties": True
}


# Define the schema for trims
car_trim_schema = {
    "type": "object",
    "properties": {
        "car_id": {
            "type": "integer",
            "minLength": 1,
            "maxLength": 50,
            "pattern": "^\d+$",
            "description": "Car car_id length at least between 1 to 50 and only allow the numbers."
            },
        "year_id": {
            "type": "integer",
            "minLength": 1,
            "maxLength": 50,
            "pattern": "^\d+$",
            "description": "Car year length at least between 1 to 50 and only allow the numbers."
            },
        "model_id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50,
            "pattern": "^\d+$",
            "description": "Car model length at least between 1 to 50 and only allow the numbers."
            },
        "car_trim_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            # "pattern": "^[a-zA-Z0-9]*$",
            "description": "Car model name length between 3 to 50 characters."
            },
    },
    "required": ["car_id", "year", "model_id", "car_trim_name"],
    "additionalProperties": True
}


# Compile the schemas
validate_car_brand = fastjsonschema.compile(car_brand_schema)
validate_car_year = fastjsonschema.compile(car_year_schema)
validate_car_model = fastjsonschema.compile(car_model_schema)
validate_car_trim = fastjsonschema.compile(car_trim_schema)