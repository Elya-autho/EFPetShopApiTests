INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["placed", "approved", "delivered"]
        }

    },
    "required": ["placed", "approved", "delivered"],
    "additionalProperties": False
}





