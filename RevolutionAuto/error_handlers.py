# error_handlers.py

def get_friendly_error_message(error_message):
    error_mappings = {
    # Email errors
    "data.email must be string": "Please enter a valid email address.",
    "data.email must match format \"email\"": "Please enter a valid email address.",
    "data.email must contain \"@\"": "Email address must contain '@' symbol.",
    "data.email must contain a domain": "Email address must have a domain (e.g., gmail.com).",
    "data.email is not a valid email address": "Please enter a valid email address.",
    "data.email must not contain spaces": "Email address must not contain spaces.",
    "data.email domain must be valid": "Email address domain is not valid.",
    "data.email cannot be a disposable email": "Please use a non-disposable email address.",
    
    # Password errors
    "data.password must be string": "Password is required.",
    "data.password must be at least 8 characters long": "Password must be at least 8 characters long.",
    "data.password must contain at least one uppercase letter": "Password must contain at least one uppercase letter.",
    "data.password must contain at least one lowercase letter": "Password must contain at least one lowercase letter.",
    "data.password must contain at least one digit": "Password must contain at least one digit.",
    "data.password must contain at least one special character": "Password must contain at least one special character (e.g., @, #, $).",
    "data.password must not contain spaces": "Password must not contain spaces.",
    
    # First name errors
    "data.first_name must be string": "First name is required.",
    "data.first_name must match pattern ^[a-zA-Z]+$": "First name should only contain letters.",
    "data.first_name must not contain numbers": "First name must not contain numbers.",
    "data.first_name must not contain special characters": "First name must not contain special characters.",
    "data.first_name must not be too short": "First name must be at least 2 characters long.",
    
    # Last name errors
    "data.last_name must be string": "Last name is required.",
    "data.last_name must match pattern ^[a-zA-Z]+$": "Last name should only contain letters.",
    "data.last_name must not contain numbers": "Last name must not contain numbers.",
    "data.last_name must not contain special characters": "Last name must not contain special characters.",
    "data.last_name must not be too short": "Last name must be at least 2 characters long.",
    
    # Phone number errors
    "data.phone_no must be string": "Phone number is required.",
    "data.phone_no must match pattern ^\\+?[1-9]\\d{1,14}$": "Please enter a valid phone number.",
    "data.phone_no must not contain letters": "Phone number must not contain letters.",
    "data.phone_no must not contain special characters": "Phone number must not contain special characters.",
    "data.phone_no must not be too short": "Phone number must be at least 7 digits long.",
    "data.phone_no must not be too long": "Phone number must not exceed 15 digits.",
    
    # Role errors
    "data.role must be string": "Role is required.",
    "data.role must be one of ['admin', 'user', 'superadmin']": "Invalid role selected.",
    "data.role must not be empty": "Role must not be empty.",
    "data.role must not contain numbers": "Role must not contain numbers.",
    "data.role must not contain special characters": "Role must not contain special characters.",
}

    for key, value in error_mappings.items():
        if key in error_message:
            return value
    
    return "An error occurred. Please check your input and try again."