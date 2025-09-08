# save_json/load_json for Thread

def save_json(thread, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(thread.model_dump_json(indent=2))

def load_json(path):
    from DGN_Agents.models import Thread
    import orjson
    with open(path, "rb") as f:
        data = orjson.loads(f.read())
    return Thread.model_validate(data)
