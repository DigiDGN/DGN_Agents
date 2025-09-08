from typing import Any, Dict, Iterator, AsyncIterator, List
import orjson
from httpx import Client, AsyncClient

def stream_sse(client: Client, url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> Iterator[Dict[str, str]]:
    content: List[str] = []
    with client.stream("POST", url, json=payload, headers=headers, timeout=None) as r:
        for line in r.iter_lines():
            if not line:
                continue
            if not line.startswith("data: "):
                continue  # skip non-data lines
            line = line[6:]  # strip 'data: '
            if line == "[DONE]":
                break
            d = orjson.loads(line)
            delta = d["choices"][0]["delta"].get("content")
            if delta:
                content.append(delta)
                yield {"delta": delta, "response": "".join(content)}

async def stream_sse_async(client: AsyncClient, url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> AsyncIterator[Dict[str, str]]:
    content: List[str] = []
    async with client.stream("POST", url, json=payload, headers=headers, timeout=None) as r:
        async for line in r.aiter_lines():
            if not line:
                continue
            if not line.startswith("data: "):
                continue  # skip non-data lines
            line = line[6:]
            if line == "[DONE]":
                break
            d = orjson.loads(line)
            delta = d["choices"][0]["delta"].get("content")
            if delta:
                content.append(delta)
                yield {"delta": delta, "response": "".join(content)}
