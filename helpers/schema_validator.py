import json
from jsonschema import validate, ValidationError
import importlib.resources as pkg_resources
from resources import schemas


def validate_schema(response: dict, schema_name: str):
    with pkg_resources.open_text(schemas, f"{schema_name}.json", encoding="utf-8") as f:
        schema = json.load(f)

    try:
        validate(instance=response, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"{e.message}")
