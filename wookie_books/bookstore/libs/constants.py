BLOCK_USER = "darth vader"

CODE = {
    "1001": "{} is not allowed to publish books on Wookie Books.",
    "1002": "Book already exists for the user.",
    "1003": "Book created successfully!",
    "1004": "Unpublished successfully!",
    "1005": "Darth Vader is not allowed to publish books.",
    "1006": "Invalid key: {}, needs to match {}"
}

BOOK_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "title": {"type": "string", "maxLength": 255},
        "description": {"type": "string"},
        "author": {"type": "object", "properties": {"id": {"type": "integer"}}},
        "cover_image": {"type": "string"},
        "price": {"type": "string"},
        "published_on": {"type": "string", "format": "date-time"},
        "published": {"type": "boolean"}
    },
    "required": ["title", "description", "price"]
}
