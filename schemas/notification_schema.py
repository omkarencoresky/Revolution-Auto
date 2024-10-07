import fastjsonschema

# User credential validation for registration
notification_schema = {
    "type": "object",
    "properties": {
        "recipient_type": {
            "type": "string",
            "minLength": 4,
            "maxLength": 20,    
            "pattern": "^[a-zA-Z ]+$",
            "description": "Please select a Recipient Type."
        },
        "recipient_email": {
            "type": "string",
            "minLength": 10,
            "maxLength": 50,
            "pattern": "^(|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$",
            "description": "Email should be between 10 to 50 characters and in a valid format."
        },
        "title": {
            "type": "string",
            "minLength": 3,
            "maxLength": 255,
            "pattern": "^[^\s]+(\s[^\s]+)*$",
            "description": "Title should be 3 to 50 characters long and blank not allowed."
        },
        "message": {
            "type": "string",
            "minLength": 3,
            "maxLength": 5000,
            "pattern": "^(.|\n)+$",
            "description": "Message should be 3 to 50 characters long and blank not allowed."
        }
    },
    "required": ["title", "message", "recipient_type"],
    "additionalProperties": True
}



validate_notification = fastjsonschema.compile(notification_schema)