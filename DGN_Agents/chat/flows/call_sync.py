# __call__ for sync: tools/no-tools routes

def invoke(chat, prompt, tools=None, **kwargs):
    session = chat.session_store.get()
    if tools:
        return session.gen_with_tools(prompt, tools=tools, **kwargs)
    else:
        return session.gen(prompt, **kwargs)
