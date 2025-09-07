import json
from jsonschema import validate, ValidationError
from importlib.resources import files

from resources import schemas


def validate_schema(response: dict, schema_name: str):
    schema_path = files(schemas).joinpath(f"{schema_name}.json")
    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    try:
        validate(instance=response, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"{e.message}")
