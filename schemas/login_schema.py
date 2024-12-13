import fastjsonschema


login_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "minLength": 10,
            "maxLength": 50,
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "description": "Email should be 10 to 50 characters and in a valid format."
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLength": 20,
            "pattern": "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[!@#%^&*()_+\\-=\\[\\]{};':\"\\\\|,.<>\\/?]).+$",
            "description": "Password must be 8-20 characters long, include at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character."
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}


forget_password_schema = {
  "type": "object",
  "properties": {
    "password": {
      "type": "string",
      "minLength": 8,
      "maxLength": 20,
      "pattern": "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[!@#%^&*()_+\\-=\\[\\]{};':\"\\\\|,.<>\\/?]).+$",
      "description": "Password must be 8-20 characters long, include at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character."
    }
  },
  "required": ["password"],
  "additionalProperties": False
}

validate_login = fastjsonschema.compile(login_schema)
validate_forget_password = fastjsonschema.compile(forget_password_schema)