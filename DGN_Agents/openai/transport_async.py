from typing import Any, Dict
from httpx import AsyncClient

async def post_json_async(client: AsyncClient, url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    r = await client.post(url, json=payload, headers=headers, timeout=None)
    return r.json()
