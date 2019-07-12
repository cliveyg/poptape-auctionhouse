import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import json
from os.path import join, dirname
from jsonschema import validate, draft7_format_checker


def assert_valid_schema(data, schema_file):
    """ Checks whether the given data matches the schema """

    schema = _load_json_schema(schema_file)
    return validate(data, schema, format_checker=draft7_format_checker)


def _load_json_schema(filename):
    """ Loads the given schema file """

    with open(filename) as schema_file:
        return json.loads(schema_file.read())
