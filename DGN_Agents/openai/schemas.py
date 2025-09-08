from typing import Any, Dict
from DGN_Agents.utils import remove_a_key

def schema_to_function(schema: Any) -> Dict[str, Any]:
    assert schema.__doc__, f"{schema.__name__} is missing a docstring."
    assert ("title" not in schema.model_fields.keys()), "`title` is reserved."
    schema_dict = schema.model_json_schema()
    remove_a_key(schema_dict, "title")
    return {"name": schema.__name__, "description": schema.__doc__, "parameters": schema_dict}
