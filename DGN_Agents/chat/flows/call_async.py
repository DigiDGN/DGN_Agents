# __call__ for async: tools/no-tools routes

async def invoke(chat, prompt, tools=None, **kwargs):
    session = chat.session_store.get()
    if tools:
        return await session.gen_with_tools_async(prompt, tools=tools, **kwargs)
    else:
        return await session.gen_async(prompt, **kwargs)
