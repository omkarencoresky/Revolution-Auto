import fastjsonschema

# location schema

add_combo_schema = {
    "type":"object",
    "properties": {
        "price":{
            "type": "string",
            "minLength":1,
            "maxLength":20,
            "pattern": "^[0-9]+$",
            "description": "Service price length in between 0-150 characters and special character not allowed."
        },
        "discount_price":{
            "type": "string",
            "minLength":1,
            "maxLength":20,
            "pattern": "^[0-9]+$",
            "description": "Offer price must be integer and character not allowed."
        },
        "combo_name":{
            "type": "string",
            "minLength":3,
            "maxLength":150,
            "pattern": "^[a-zA-Z ]+$",
            "description": "Combo name length in between 3-150 characters and special character not allowed."
        },
        "start_date":{
            "type": "string",
            "minLength":8,
            "maxLength":150,
            "pattern": "^[0-9-]+$",
            "description": "Start Date length in between 8-150 characters and special character not allowed."            
        },
        "end_date":{
            "type": "string",
            "minLength":8,
            "maxLength":150,
            "pattern": "^[0-9-]+$",
            "description": "End Date length in between 8-150 characters and special character not allowed."            
        },
        "usage_limit":{
            "type": "integer",
            "minLength":1,
            "maxLength":10,
            "pattern": "^[1-9]+$",
            "description": "Usage limit grater than 1 characters and alphabets are not allowed."            
        },
            "discount_percentage": {
            "type": "number",
            "minimum": 0.01,
            "maximum": 100.0,
            "description": "Discount percentage must be a numeric value greater than 0 and up to 100."
        }
    },
    "required":["combo_name", "price", "discount_price", "start_date", "end_date", "usage_limit", "discount_percentage"],
    "additionalProperties": True
}



purchased_combo_schema = {
    "type":"object",
    "properties": {
        "combo_price":{
            "type": "string",
            "minLength":1,
            "maxLength":150,
            "pattern": "^[0-9]+$",
            "description": "Combo price must be integer and character not allowed."
        },
        "combo_name":{
            "type": "string",
            "minLength":1,
            "maxLength":150,
            "pattern": "^[a-zA-Z ]+$",
            "description": "Combo name length in between 3-150 characters and special character not allowed."
        },
        "car_id":{
            "type": "string",
            "minLength":1,
            "maxLength":20,
            "pattern": "^[0-9]+$",
            "description": "Car Id must be integer and character not allowed."            
        },
    },
    "required":["combo_price", "combo_name", "car_id"],
    "additionalProperties": True
}



booking_appointment_schema = {
    "type":"object",
    "properties": {
        "service":{
            "type": "string",
            "minLength":1,
            "maxLength":20,
            "pattern": "^[0-9]+$",
            "description": "Service must be an integer and character not allowed."
        },
        "service_type":{
            "type": "string",
            "minLength":1,
            "maxLength":20,
            "pattern": "^[0-9]+$",
            "description": "Service Type must be an integer and character not allowed."
        },
        "service_category":{
            "type": "string",
            "minLength":1,
            "maxLength":150,
            "pattern": "^[0-9]+$",
            "description": "Service Category must be an integer and character not allowed."
        },
        "combo_id":{
            "type": "string",
            "minLength":1,
            "maxLength":150,
            "pattern": "^[0-9-]+$",
            "description": "Combo must be an integer and character not allowed.",
        },
        "location":{
            "type": "string",
            "minLength":1,
            "maxLength":150,
            "pattern": "^[0-9]+$",
            "description": "Location must be an integer and character not allowed.",
        },
        "sub_service": {
        "type": "object",
        "description": "Sub Service must be an integer and character not allowed.",
        "patternProperties": {
            "^[0-9]+$": {
            "type": "string",
            "pattern": "^[0-9 ]+$",
            "description": "Sub Service option must be an integer and character not allowed."
            }
        },
        "additionalProperties": True
        }
    },
    "required":["service", "service_type", "service_category", "combo_id", "location", "sub_service"],
    "additionalProperties": True
}


# Compile location schema
validate_add_combo_schema = fastjsonschema.compile(add_combo_schema)
validate_purchased_combo_schema = fastjsonschema.compile(purchased_combo_schema)
validate_booking_appointment_schema = fastjsonschema.compile(booking_appointment_schema)