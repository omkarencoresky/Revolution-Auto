import fastjsonschema

registration_schema = {
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z]+$",  # Only alphabets
            "description": "First name should be 3 to 50 characters long and contain only letters."
        },
        "last_name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "pattern": "^[a-zA-Z]+$",  # Only alphabets
            "description": "Last name should be 3 to 50 characters long and contain only letters."
        },
        "email": {
            "type": "string",
            "minLength": 10,
            "maxLength": 50,    
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",  # Standard email pattern
            "description": "Email should be between 10 to 50 characters and in a valid format.. Example."
        },
        "phone_no": {
            "type": "string",
            "minLength": 10,
            "maxLength": 13,
            "pattern": "^[0-9]+$" , # Only numbers
            "description": "Contact number should be between 10 to 13 digits, starting with +91: Example."
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLength": 20,
            "pattern":  "[A-Za-z\d!@#%^&*()_+\-=\[\]{};':\\|,.<>/?]",
            "description": "Password should be 8 to 20 characters long, with at least 1 uppercase letter and 1 special character."
        }
    },
    "required": ["first_name", "last_name", "email", "password", "phone_no"],
    "additionalProperties": True
}


validate_registration = fastjsonschema.compile(registration_schema)     