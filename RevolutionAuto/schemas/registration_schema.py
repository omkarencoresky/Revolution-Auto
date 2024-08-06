import fastjsonschema

registration_schema = {
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z]+$",  # Only alphabets
            "description": "First Name minmum length 3 and maximum 50 and only allow alphabets. Example: user"
        },
        "last_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z]+$",  # Only alphabets
            "description": "Last Name minmum length 3 and maximum 50 and only allow alphabets. Example: user"
        },
        "email": {
            "type": "string",
            "minLength": 10,
            "maxLength": 50,    
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",  # Standard email pattern
            "description": "Email address minmum length 10 and maximum 50. Example: user@example.com"
        },
        "phone_no": {
            "type": "string",
            "minLength": 10,
            "maxLength": 13,
            "pattern": "^[0-9]+$" , # Only numbers
            "description": "Contact Number minmum length 10 and maximum 13 with (+91). Example: 123456123, +91 2587469654"
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLength": 20,
            "description": "Password minmum length 8 and maximum 20. Example: user@123"
        }
    },
    "required": ["first_name", "last_name", "email", "password", "phone_no"],
    "additionalProperties": True
}

validate_registration = fastjsonschema.compile(registration_schema)     