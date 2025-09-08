from typing import Any, Dict, Optional
from httpx import Client

def post_json(client: Client, url: str, payload: Dict[str, Any], headers: Dict[str, str], timeout: Optional[float] = None) -> Dict[str, Any]:
    r = client.post(url, json=payload, headers=headers, timeout=timeout)
    return r.json()
