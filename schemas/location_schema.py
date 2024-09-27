import fastjsonschema

# location schema

location_schema = {
    "type":"object",
    "properties": {
        "location_name":{
            "type": "string",
            "minLength":3,
            "maxLength":150,
            "pattern": "^[a-zA-Z0-9 ]+$",
            "description": "Location name length in between 3-150 characters and special character not allowed."
        },
        "country_code":{
            "type":"string",
            "minLength":2,
            "maxLength":50,
            "pattern": "^[a-zA-Z0-9 ]+$",
            "description": "Country code length in between 2-50 characters and special character not allowed."
        },
        "service_availability":{
            "type":"boolean",
            "description": "In-valid service status choose, try again."            
        }
    },
    "required":["location_name", "country_code", "service_availability"],
    "additionalProperties": True
}

# Compile location schema
validate_location_schema = fastjsonschema.compile(location_schema)