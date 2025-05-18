STORE_SCHEMA = {
    "type": "object",
    "properties":{
        "id":{
            "type": "integer"
        },
        "petId":{
            "type": "integer"
        },
        "quantity":{
            "type": "integer"
        },
        "shipDate":{
            "type": "string",
            "format": "date-time"
        },
        "status":{
            "type": "string",
            "enum": ["placed", "approved", "delivered"]
        },
        "complete":{
            "type": "boolean"
        }
    },

    "required": ["id", "petId", "quantity",  "status", "complete"],
     "additionalProperties": False

}