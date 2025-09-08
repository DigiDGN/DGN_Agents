from typing import Any, Dict, List, Optional
from httpx import Client, AsyncClient

from DGN_Agents.models import Thread, Turn
from .config import resolve_provider
from .headers import build_headers
from .payload import build_messages, add_functions_payload
from .responses import parse_completion
from .sse import stream_sse, stream_sse_async
from .transport_sync import post_json
from .transport_async import post_json_async
from . import legacy as legacy_tools


class OpenAISession(Thread):
    system: str = "You are a helpful assistant."
    wire_fields = {"role", "content", "name"}
    api_url: Optional[str] = "https://api.openai.com/v1/chat/completions"
    params: Dict[str, Any] = {"temperature": 0.7}

    def prepare_request(
        self,
        prompt: str,
        system: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        input_schema: Any = None,
        output_schema: Any = None,
        is_function_calling_required: bool = True,
    ):
        resolved = resolve_provider(self, params)
        assert resolved["api_key"], "API key required."
        assert resolved["model"], "Model name required."

        headers = build_headers(resolved["api_key"])
        msgs, user_turn = build_messages(self, system, prompt, input_schema)
        data: Dict[str, Any] = {"model": resolved["model"], "messages": msgs, "stream": stream, **resolved["params"]}
        add_functions_payload(data, input_schema, output_schema, is_function_calling_required)
        return headers, data, user_turn, resolved["api_url"]

    # sync
    def gen(self, prompt: str, client: Client, system: Optional[str] = None,
            save_messages: Optional[bool] = None, params: Optional[Dict[str, Any]] = None,
            input_schema: Any = None, output_schema: Any = None):
        headers, data, user_turn, api_url = self.prepare_request(prompt, system, params, False, input_schema, output_schema)
        r = post_json(client, api_url, data, headers)
        content, assistant_turn = parse_completion(r, output_schema)
        if assistant_turn:
            self.add_messages(user_turn, assistant_turn, save_messages)
        return content

    def stream(self, prompt: str, client: Client, system: Optional[str] = None,
               save_messages: Optional[bool] = None, params: Optional[Dict[str, Any]] = None,
               input_schema: Any = None):
        headers, data, user_turn, api_url = self.prepare_request(prompt, system, params, True, input_schema)
        collected: List[str] = []
        for delta in stream_sse(client, api_url, data, headers):
            if "delta" in delta:
                collected.append(delta["delta"])
                yield delta
        assistant_turn = Turn(role="assistant", content="".join(collected))
        self.add_messages(user_turn, assistant_turn, save_messages)
        return assistant_turn

    # async
    async def gen_async(self, prompt: str, client: AsyncClient, system: Optional[str] = None,
                        save_messages: Optional[bool] = None, params: Optional[Dict[str, Any]] = None,
                        input_schema: Any = None, output_schema: Any = None):
        headers, data, user_turn, api_url = self.prepare_request(prompt, system, params, False, input_schema, output_schema)
        r = await post_json_async(client, api_url, data, headers)
        content, assistant_turn = parse_completion(r, output_schema)
        if assistant_turn:
            self.add_messages(user_turn, assistant_turn, save_messages)
        return content

    async def stream_async(self, prompt: str, client: AsyncClient, system: Optional[str] = None,
                           save_messages: Optional[bool] = None, params: Optional[Dict[str, Any]] = None,
                           input_schema: Any = None):
        headers, data, user_turn, api_url = self.prepare_request(prompt, system, params, True, input_schema)
        collected: List[str] = []
        async for delta in stream_sse_async(client, api_url, data, headers):
            if "delta" in delta:
                collected.append(delta["delta"])
                yield delta
        assistant_turn = Turn(role="assistant", content="".join(collected))
        self.add_messages(user_turn, assistant_turn, save_messages)

    # LEGACY tool router (kept as-is, clearly marked)
    gen_with_tools = legacy_tools.gen_with_tools
    gen_with_tools_async = legacy_tools.gen_with_tools_async
