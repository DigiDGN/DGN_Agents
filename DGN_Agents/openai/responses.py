from typing import Any, Dict, Tuple
import orjson
from DGN_Agents.models import Turn

def parse_completion(r: Dict[str, Any], output_schema: Any = None) -> Tuple[Any, Optional[Turn]]:
    if not output_schema:
        choice = r["choices"][0]
        msg = choice["message"]
        content = msg["content"]
        t = Turn(
            role=msg["role"],
            content=content,
            stop=choice.get("finish_reason"),
            tokens={
                "prompt": r["usage"]["prompt_tokens"],
                "completion": r["usage"]["completion_tokens"],
                "total": r["usage"]["total_tokens"],
            },
            # legacy mirrors (Thread.append keeps totals synced)
            finish_reason=choice.get("finish_reason"),
            prompt_length=r["usage"]["prompt_tokens"],
            completion_length=r["usage"]["completion_tokens"],
            total_length=r["usage"]["total_tokens"],
        )
        return content, t
    else:
        args = r["choices"][0]["message"]["function_call"]["arguments"]
    return orjson.loads(args), None
