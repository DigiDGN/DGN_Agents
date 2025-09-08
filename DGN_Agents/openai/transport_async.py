from typing import Any, Dict, Optional
from httpx import AsyncClient

async def post_json_async(client: AsyncClient, url: str, payload: Dict[str, Any], headers: Dict[str, str], timeout: Optional[float] = None) -> Dict[str, Any]:
    r = await client.post(url, json=payload, headers=headers, timeout=timeout)
    return r.json()
