
import os
from uuid import uuid4
from httpx import AsyncClient
from contextlib import asynccontextmanager
from DGN_Agents.chat.sessions.store import SessionStore
from DGN_Agents.chat.sessions.factory import new_session
from DGN_Agents.chat.sessions.context import async_session_context
from DGN_Agents.chat.flows.call_async import invoke as call_invoke
from DGN_Agents.chat.flows.stream_async import stream as stream_invoke
from DGN_Agents.chat.persist.json_io import save_json, load_json
from DGN_Agents.chat.persist.csv_io import save_csv, load_csv

class AsyncAIChat:
    def __init__(self, system=None, model_cfg=None, **kwargs):
        self.client = AsyncClient(proxies=os.getenv("https_proxy"))
        self.session_store = SessionStore()
        self.new_session(system=system, model_cfg=model_cfg, **kwargs)

    def new_session(self, **kwargs):
        session = new_session(**kwargs)
        self.session_store.add(session)
        self.session_store.set_default(session.id)
        return session

    def get_session(self, id=None):
        return self.session_store.get(id)

    def reset_session(self, id=None):
        session = self.get_session(id)
        session.messages = []

    def delete_session(self, id=None):
        self.session_store.delete(id)

    @asynccontextmanager
    async def session(self, **kwargs):
        async with async_session_context(self.session_store, **kwargs) as sess:
            yield sess

    async def __call__(self, prompt, tools=None, **kwargs):
        return await call_invoke(self, prompt, tools=tools, **kwargs)

    async def stream(self, prompt, **kwargs):
        async for delta in stream_invoke(self, prompt, **kwargs):
            yield delta

    def save_json(self, id=None, path=None):
        session = self.get_session(id)
        save_json(session, path or f"chat_session_{session.id}.json")

    def load_json(self, path, set_default=True):
        session = load_json(path)
        self.session_store.add(session)
        if set_default:
            self.session_store.set_default(session.id)
        return session

    def save_csv(self, id=None, path=None):
        session = self.get_session(id)
        save_csv(session, path or f"chat_session_{session.id}.csv")

    def load_csv(self, path, set_default=True):
        session = load_csv(path)
        self.session_store.add(session)
        if set_default:
            self.session_store.set_default(session.id)
        return session
