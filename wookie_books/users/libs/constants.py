CODE = {
    "101": "username is required",
    "102": "password is required",
    "103": "author_pseudonym is required",
    "104": "author_pseudonym already exists",
    "105": "Username already exists",
    "106": "User registered successfully!",
    "107": "Invalid credentials"
}

CUSTOM_USER_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 3
        },
        "author_pseudonym": {
            "type": "string",
            "minLength": 3
        },
        "created_on": {
            "type": "string",
            "format": "date-time"
        },
        "updated_on": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "username",
        "author_pseudonym",
        "created_on",
        "updated_on"
    ]
}
