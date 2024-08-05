import fastjsonschema

registration_schema = {
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "pattern": "^[a-zA-Z]+$"  # Only alphabets
        },
        "last_name": {
            "type": "string",
            "pattern": "^[a-zA-Z]+$"  # Only alphabets
        },
        "email": {
            "type": "string",
            "format": "email"  # Validates standard email format
        },
        "password": {
            "type": "string",
            "minLength": 20  # Password must be at least 20 characters long
        },
        "phone_no": {
            "type": "string",
            "pattern": "^[0-9]+$"  # Only numbers
        }
    },
    "required": ["first_name", "last_name", "email", "password", "phone_no"],
    "additionalProperties": True
}

validate_registration = fastjsonschema.compile(registration_schema) 