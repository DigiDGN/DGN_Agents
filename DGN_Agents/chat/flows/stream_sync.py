# stream generator (sync)

def stream(chat, prompt, **kwargs):
    session = chat.session_store.get()
    yield from session.stream(prompt, **kwargs)
