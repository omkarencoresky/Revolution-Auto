import fastjsonschema

quote_data_schema = {
    "type": "object",
    "properties": {
        "service_location": {
            "type": "string",
            "minimum": 1,
            "maximum": 99999,
            "pattern": "^[0-9]+$",
            "description": "Booking not saved due to, selected service_location is not a valid option"
        },
        "car_brand": {
            "type": "string",
            "minimum": 1,
            "maximum": 99999,
            "pattern": "^[0-9]+$",
            "description": "Booking not saved due to, selected car_brand is not a valid option"
        },
        "car_year": {
            "type": "string",
            "minimum": 1,
            "maximum": 99999,
            "pattern": "^[0-9]+$",
            "description": "Booking not saved due to, selected car_year is not a valid option"
        },
        "car_model": {
            "type": "string",
            "minimum": 1,
            "maximum": 99999,
            "pattern": "^[0-9]+$",
            "description": "Booking not saved due to, selected car_model is not a valid option"
        },
        "car_trim": {
            "type": "string",
            "minimum": 1,
            "maximum": 99999,
            "pattern": "^[0-9]+$",
            "description": "Booking not saved due to, selected car_trim is not a valid option"
        },
        "car_service_type": {
            "type": "string",
            "minimum": 1,
            "maximum": 99999,
            "pattern": "^[0-9]+$",
            "description": "Booking not saved due to, selected car_service_type is not a valid option"
        },
        "car_service_category": {
            "type": "string",
            "minimum": 1,
            "maximum": 99999,
            "pattern": "^[0-9]+$",
            "description": "Booking not saved due to, selected car_service_category is not a valid option"
        },
        "service_list": {
          "type": "array",
          "description": "Booking not saved due to, selected services is not a valid option",
          "items": {
            "type": "string",
            "pattern": "^[0-9]+$",
          },
        },
        "sub_service_list": {
          "type": "array",
          "description": "Booking not saved due to, selected sub service is not a valid option",
          "items": {
            "type": "string",
            "pattern": "^[0-9]+$",
          },
        },
        "sub_service_option_list": {
          "type": "array",
          "description": "Booking not saved due to, selected sub service option is not a valid option",
          "items": {
            "type": "string",
            "pattern": "^[0-9]+$",
          },
        },

    },
    "required": ["service_location", "car_brand", "car_year", "car_model", "car_trim", "car_service_type", "car_service_category", "service_list"],
    "additionalProperties": True
}


quote_sub_service_option_data_schema = {
    "type": "object",
    "properties": {
        "car_service_type": {
            "type": "string",
            "minimum": 1,
            "maximum": 99999,
            "pattern": "^[0-9]+$",
            "description": "Booking not saved due to, selected car_service_type is not a valid option"
        },
        "car_service_category": {
            "type": "string",
            "minimum": 1,
            "maximum": 99999,
            "pattern": "^[0-9]+$",
            "description": "Booking not saved due to, selected car_service_category is not a valid option"
        },
        "service_list": {
          "type": "array",
          "description": "Booking not saved due to, selected services is not a valid option",
          "items": {
            "type": "string",
            "pattern": "^[0-9]+$",
          },
        },
        "sub_service_list": {
          "type": "array",
          "description": "Booking not saved due to, selected sub service is not a valid option",
          "items": {
            "type": "string",
            "pattern": "^[0-9]+$",
          },
        },
        "sub_service_option_list": {
          "type": "array",
          "description": "Booking not saved due to, selected sub service option is not a valid option",
          "items": {
            "type": "string",
            "pattern": "^[0-9]+$",
          },
        },
    },
    "required": [],
    "additionalProperties": True
}



# Define the schema for Update quote price
quote_price_schema = {
    "type": "object",
    "properties": {
        "parts_amount": {
            "type": "number",
            "minimum": 0,
            "maximum": 999999.99,
            "multipleOf": 0.01,
            "description": "Part's price should be greater than '0' a number"
        },
        "labour_amount": {    # Changed from image_format to better reflect its purpose
            "type": "number",
            "minimum": 0,
            "maximum": 999999.99,
            "multipleOf": 0.01,
            "description": "Labour price should be greater than '0' a number"
        },
        "total_service_amount": {
            "type": "number",
            "minimum": 0,
            "maximum": 999999.99,
            "multipleOf": 0.01,
            "description": "Total price should be greater than '0' and a number"
        }
    },
    "required": ["parts_amount", "labour_amount", "total_service_amount"],
    "additionalProperties": True
}



car_detail_schema = {
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": [
        "quoted", "scheduled", "completed", "pending for quote", 
        "progressing", "pending", "deleted", "cancelled"
      ],
      "description": "In-valid booking status"
    },
    "car_vno": {
      "type": "string",
      "minLength": 16,
      "maxLength": 16,
      "pattern": "^[0-9]+$",
      "description": "The Vehicle Identity Number (VNO) must be 16 digits only"
    }
  },
  "if": {
    "properties": { "car_vno": { "type": "string" } }
  },
  "then": {
    "properties": {
      "car_vno": { 
        "type": "string", 
        "minLength": 16, 
        "maxLength": 16, 
        "pattern": "^[0-9]+$" 
      }
    }
  },
  "else": {
    "properties": {
      "status": {
        "type": "string",
        "enum": [
          "quoted", "scheduled", "completed", "pending for quote", 
          "progressing", "pending", "deleted", "cancelled"
        ]
      }
    }
  },
  "additionalProperties": False
}



# card_data_schema = {
#     "type": "object",
#     "properties": {
#         "customer_name": {
#             "type": "string",
#             "minLength": 1,
#             "maxLength": 100,
#             "pattern": "^[a-zA-Z .-]+$",
#             "description": "Customer name must contain only letters, spaces, dots, and hyphens"
#         },
#         "customer_address": {
#             "type": "string",
#             "minLength": 1,
#             "maxLength": 200,
#             "pattern": "^[a-zA-Z0-9 ,.-]+$",
#             "description": "Address must contain only alphanumeric characters, spaces, commas, dots, and hyphens"
#         },
#         "card_no": {
#             "type": "string",
#             "minLength": 16,
#             "maxLength": 16,
#             "pattern": "^[0-9]{16}$",
#             "description": "Card number must be exactly 16 digits"
#         },
#         "expiry_date": {
#             "type": "string",
#             "pattern": "^(0[1-9]|1[0-2])\/([0-9]{2})$",
#             "description": "Expiry date must be in MM/YY format"
#         },
#         "cvv": {
#             "type": "string",
#             "minLength": 3,
#             "maxLength": 3,
#             "pattern": "^[0-9]{3}$",
#             "description": "CVV must be exactly 3 digits"
#         }
#     },
#     "required": ["customer_name", "customer_address", "card_no", "expiry_date", "cvv"],
#     "additionalProperties": True
# }




# Compile the schemas
validate_quote_price = fastjsonschema.compile(quote_price_schema)
validate_car_detail = fastjsonschema.compile(car_detail_schema)
validate_quote_data = fastjsonschema.compile(quote_data_schema)
# validate_card_data = fastjsonschema.compile(card_data_schema)
validate_quote_sub_service_option_data_schema = fastjsonschema.compile(quote_sub_service_option_data_schema)