# stream generator (async)

async def stream(chat, prompt, **kwargs):
    session = chat.session_store.get()
    async for delta in session.stream_async(prompt, **kwargs):
        yield delta
