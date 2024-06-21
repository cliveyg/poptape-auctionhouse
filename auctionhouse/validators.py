from django.core.exceptions import ValidationError
from jsonschema.exceptions import ValidationError as JsonValidatonError
#from django.utils.translation import gettext_lazy as _
from django.conf import settings
#from rest_framework import serializers
from jsonschema import validate
import json
import re
from auctionhouse.assertions import assert_valid_schema
import os.path

# get an instance of a logger
import logging
logger = logging.getLogger('apiserver')

# -----------------------------------------------------------------------------

def validate_currency(value):
    pass

# -----------------------------------------------------------------------------

def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(
            ('%(value)s is not an integer or a number to two decimal places'),
            params={'value': value},
        )


# -----------------------------------------------------------------------------

def validate_uuid_from_model(value):
    #uuid_json = '{ "uuid": "'+value+'" }'
    #json_schema_validation(uuid_json, '/schemas/uuid.json')
    # [0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}
    if re.match("[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", value):
        pass
    else:
        raise ValidationError("Input is not a valid UUID")

# -----------------------------------------------------------------------------

def json_schema_validation(data, schema_uri):

    try:
        json_data = json.loads(data)
    except:
        raise ValidationError("Input is not valid json")

    # not fussed about being super quick here as validating urls when 
    # creating api paths is not an everyminute occurence only when
    # creating a record
    filepath = os.path.abspath(os.path.dirname(__file__))
    full_filename = filepath + schema_uri

    try:
        assert_valid_schema(json_data, full_filename)
    except JsonValidatonError as error:
        raise ValidationError(error.message)

