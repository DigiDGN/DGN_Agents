# Constructs new OpenAISession with ModelCfg

def new_session(model_cfg, system_prompt, **kwargs):
    from DGN_Agents.openai import OpenAISession
    return OpenAISession(model_cfg=model_cfg, system=system_prompt, **kwargs)
