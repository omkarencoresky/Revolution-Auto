import fastjsonschema


login_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "minLength": 10,
            "maxLength": 50,
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "description": "Email must be 10 to 50 characters and in a valid format."
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLength": 20,
            "pattern":  "[A-Za-z\d!@#%^&*()_+\-=\[\]{};':\\|,.<>/?]",
            "description": "Password must be 8 to 20 characters long, with at least 1 uppercase letter and 1 special character."
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}

validate_login = fastjsonschema.compile(login_schema)