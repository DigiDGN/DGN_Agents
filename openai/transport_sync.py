from typing import Any, Dict
from httpx import Client

def post_json(client: Client, url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    r = client.post(url, json=payload, headers=headers, timeout=None)
    return r.json()
