from typing import Any, Dict, Optional
from DGN_Agents.models import Thread

def resolve_provider(thread: Thread, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    # model
    model = getattr(thread, "model", None)
    if getattr(thread, "model_cfg", None) and getattr(thread.model_cfg, "name", None):
        model = thread.model_cfg.name or model

    # api url
    api_url = getattr(thread, "api_url", None)
    if getattr(thread, "model_cfg", None) and getattr(thread.model_cfg, "api_url", None):
        api_url = str(thread.model_cfg.api_url) or api_url

    # params (merge order: thread.params < model_cfg.params < call params)
    merged: Dict[str, Any] = {}
    merged.update(getattr(thread, "params", {}) or {})
    if getattr(thread, "model_cfg", None) and getattr(thread.model_cfg, "params", None):
        merged.update(thread.model_cfg.params or {})
    merged.update(params or {})

    # auth (prefer model_cfg.auth, fallback to thread.auth)
    api_key = None
    if getattr(thread, "model_cfg", None) and getattr(thread.model_cfg, "auth", None):
        if "api_key" in thread.model_cfg.auth:
            api_key = thread.model_cfg.auth["api_key"].get_secret_value()
    if api_key is None and getattr(thread, "auth", None):
        if "api_key" in thread.auth:
            api_key = thread.auth["api_key"].get_secret_value()

    return {"model": model, "api_url": api_url, "params": merged, "api_key": api_key}
