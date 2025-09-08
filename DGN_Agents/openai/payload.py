from typing import Any, Dict, List, Optional, Tuple
from DGN_Agents.models import Thread, Turn
from .schemas import schema_to_function

def build_messages(thread: Thread, system: Optional[str], prompt: str, input_schema: Any = None) -> Tuple[List[Dict[str, Any]], Turn]:
    system_turn = Turn(role="system", content=system or thread.system)
    if not input_schema:
        user_turn = Turn(role="user", content=prompt)
    else:
        assert isinstance(prompt, input_schema), f"prompt must be an instance of {input_schema.__name__}"
        user_turn = Turn(role="function", content=prompt.model_dump_json(), name=input_schema.__name__)
    return thread.format_for_provider(system_turn, user_turn), user_turn

def add_functions_payload(data: Dict[str, Any], input_schema: Any = None, output_schema: Any = None, require_output_call: bool = True) -> None:
    if not (input_schema or output_schema):
        return
    functions = []
    if input_schema:
        functions.append(schema_to_function(input_schema))
    if output_schema:
        out_fn = schema_to_function(output_schema)
        if out_fn not in functions:
            functions.append(out_fn)
        if require_output_call:
            data["function_call"] = {"name": output_schema.__name__}
    data["functions"] = functions
