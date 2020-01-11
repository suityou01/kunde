new_org_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "name": {
            "description": "The name of the organisation",
            "type": "string",
            "maxLength": 250
        },
        "address_1": {
            "description": "The first line of the organisation's address",
            "type": "string",
            "maxLength": 250
        },
        "address_2": {
            "description": "The second line of the organisation's address",
            "type": "string",
            "maxLength": 250
        },
        "town": {
            "description": "The town of the organisation's address",
            "type": "string",
            "maxLength": 250
        },
        "state": {
            "description": "The state or county of the organisation's address",
            "type": "string",
            "maxLength": 250
        },
        "zip": {
            "description": "The zip or postal code of the organisation's address",
            "type": "string",
            "maxLength": 250
        },
        "country": {
            "description": "The country of the organisation's address",
            "type": "number"
        },
        "username" : {
            "description": "The username of the user creating the organisation"
        }
    },
    "required": ["name", "username", "address_1", "town", "zip"],
    "additionalProperties": False
}

update_org_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description" : "The primary key of the organisation record",
            "type": "number"
        },
        "name": {
            "description": "The name of the organisation",
            "type": "string",
            "maxLength": 250
        },
        "username" : {
            "description": "The username of the user creating the organisation"
        }
    },
    "required": ["org_id", "name", "username"],
    "additionalProperties": False
}

delete_org_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description" : "The primary key of the organisation record",
            "type": "number"
        },
        "username" : {
            "description": "The username of the user creating the organisation"
        }
    },
    "required": ["org_id", "username"],
    "additionalProperties": False
}

search_org_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description": "The primary key of the organisation record",
            "type": "number"
        },
        "name": {
            "description": "The name of the organisation",
            "type": "string",
            "maxLength": 250
        },
        "zip": {
            "description": "The zip or postal code of the organisation's address",
            "type": "string",
            "maxLength": 250
        },
        "include_inactive": {
            "description": "Flag if true include deleted organisations in the search",
            "type": "boolean"
        }
    },
    "required": ["include_inactive"],
    "additionalProperties": False
}

new_org_person_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description": "The primary key of the organisation record",
            "type": "number"
        },
        "person_id": {
            "description": "The id of the person record",
            "type": "number"
        },
        "first": {
            "description": "The first name of the person to be added",
            "type": "string",
            "maxLength": 250
        },
        "last": {
            "description": "The last name of the person to be added",
            "type": "string",
            "maxLength": 250
        },
        "rel_type": {
            "description": "The id of the org person relationship type",
            "type": "number"
        },
        "username": {
            "description": "The username of the user adding the record",
            "type": "string",
            "maxLength": 50
        }
    },
    "required": ["org_id", "rel_type", "username"],
    "additionalProperties": False
}

remove_org_person_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description": "The primary key of the organisation record",
            "type": "number"
        },
        "person_id": {
            "description": "The primary key of the organisation record",
            "type": "number"
        },
        "reason": {
            "description": "The reason the user is removing the person",
            "type": "string",
            "maxLength": 250
        },
        "username": {
            "description": "The username of the user adding the record",
            "type": "string",
            "maxLength": 50
        }
    },
    "required": ["org_id", "person_id", "username"],
    "additionalProperties": False
}

search_org_person_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description": "The primary key of the organisation record",
            "type": "number"
        },
        "include_inactive": {
            "description": "Flag if true include deleted organisations in the search",
            "type": "boolean"
        }
    },
    "required": ["org_id", "include_inactive"],
    "additionalProperties": False
}

new_org_contact_route_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description": "The primary key of the organisation record",
            "type": "number"
        },
        "name": {
            "description": "The name of the contact route to be added",
            "type": "string",
            "maxLength": 50
        },
        "value": {
            "description": "The value of the contact route to be added",
            "type": "string",
            "maxLength": 50
        },
        "contact_route_type": {
            "description": "The foreign key of the contact route type",
            "type": "number"
        },
        "username": {
            "description": "The username of the user adding the record",
            "type": "string",
            "maxLength": 50
        }
    },
    "required": ["org_id", "name", "value", "contact_route_type"],
    "additionalProperties": False
}

update_org_contact_route_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "contact_route_id": {
            "description": "The primary key of the contact route record",
            "type": "number"
        },
        "name": {
            "description": "The name of the contact route to be added",
            "type": "string",
            "maxLength": 50
        },
        "value": {
            "description": "The value of the contact route to be added",
            "type": "string",
            "maxLength": 50
        },
        "username": {
            "description": "The username of the user adding the record",
            "type": "string",
            "maxLength": 50
        }
    },
    "required": ["contact_route_id", "name", "value"],
    "additionalProperties": False
}

delete_org_contact_route_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "contact_route_id": {
            "description": "The primary key of the contact route record",
            "type": "number"
        },
        "username": {
            "description": "The username of the user adding the record",
            "type": "string",
            "maxLength": 50
        }
    },
    "required": ["contact_route_id"],
    "additionalProperties": False
}

read_org_contact_route_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description": "The primary key of the contact route record",
            "type": "number"
        },
        "include_inactive": {
            "description": "Flag if true include deleted organisations in the search",
            "type": "boolean"
        }
    },
    "required": ["org_id", "include_inactive"],
    "additionalProperties": False
}

new_org_address_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description": "The primary key of the organisation record",
            "type": "number"
        },
        "address_1": {
            "description": "The first line of the address to be added",
            "type": "string",
            "maxLength": 250
        },
        "address_2": {
            "description": "The second line of the address to be added",
            "type": "string",
            "maxLength": 250
        },
        "town": {
            "description": "The town of the address to be added",
            "type": "string",
            "maxLength": 250
        },
        "state": {
            "description": "The state or county of the address to be added",
            "type": "string",
            "maxLength": 250
        },
        "zip": {
            "description": "The zip or postal code of the address to be added",
            "type": "string",
            "maxLength": 250
        },
        "country_id": {
            "description": "The foreign key of the country table",
            "type": "number"
        },
        "address_type_id": {
            "description": "The foreign key of the address type table",
            "type": "number"
        },
        "username": {
            "description": "The username of the user adding the record",
            "type": "string",
            "maxLength": 50
        }
    },
    "required": ["org_id", "address_1", "town", "country_id", "address_type_id", "username"],
    "additionalProperties": False
}

update_org_address_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "contact_route_id": {
            "description": "The primary key of the contact route record",
            "type": "number"
        },
        "address_1": {
            "description": "The first line of the address to be added",
            "type": "string",
            "maxLength": 250
        },
        "address_2": {
            "description": "The second line of the address to be added",
            "type": "string",
            "maxLength": 250
        },
        "town": {
            "description": "The town of the address to be added",
            "type": "string",
            "maxLength": 250
        },
        "state": {
            "description": "The state or county of the address to be added",
            "type": "string",
            "maxLength": 250
        },
        "zip": {
            "description": "The zip or postal code of the address to be added",
            "type": "string",
            "maxLength": 250
        },
        "country_id": {
            "description": "The foreign key of the country table",
            "type": "number"
        },
        "username": {
            "description": "The username of the user adding the record",
            "type": "string",
            "maxLength": 50
        }
    },
    "required": ["contact_route_id", "address_1", "town", "country_id", "username"],
    "additionalProperties": False
}

delete_org_address_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "contact_route_id": {
            "description": "The primary key of the contact route record",
            "type": "number"
        },
        "username": {
            "description": "The username of the user adding the record",
            "type": "string",
            "maxLength": 50
        }
    },
    "required": ["contact_route_id", "username"],
    "additionalProperties": False
}

read_org_address_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description": "The primary key of the contact route record",
            "type": "number"
        },
        "include_inactive": {
            "description": "Flag if true include deleted organisations in the search",
            "type": "boolean"
        }
    },
    "required": ["org_id", "include_inactive"],
    "additionalProperties": False
}

new_org_doc_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description": "The primary key of the organisation record",
            "type": "number"
        },
        "document_id": {
            "description": "The foreign key of the document type table",
            "type": "number"
        },
        "username": {
            "description": "The username of the user adding the record",
            "type": "string",
            "maxLength": 50
        }
    },
    "required": ["org_id", "document_id", "username"],
    "additionalProperties": False
}

search_org_doc_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://kunde.com/schemas/org.json",
    "title": "Organisation",
    "description": "An organisation",
    "type": "object",
    "properties": {
        "org_id": {
            "description": "The primary key of the organisation record",
            "type": "number"
        },
        "include_inactive": {
            "description": "Flag if true include deleted organisations in the search",
            "type": "boolean"
        }
    },
    "required": ["org_id", "include_inactive"],
    "additionalProperties": False
}