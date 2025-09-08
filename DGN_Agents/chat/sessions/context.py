# Context managers for temporary sessions
from contextlib import contextmanager, asynccontextmanager

@contextmanager
def session_context(store, **kwargs):
    prev_id = store.default_id
    session = store.add(store, **kwargs)
    try:
        yield session
    finally:
        store.set_default(prev_id)

@asynccontextmanager
async def async_session_context(store, **kwargs):
    prev_id = store.default_id
    session = store.add(store, **kwargs)
    try:
        yield session
    finally:
        store.set_default(prev_id)
