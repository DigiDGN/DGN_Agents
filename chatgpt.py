# DGN_Agents/chatgpt.py
# Thin shim for backward-compatibility with older imports.
# The real implementation now lives in DGN_Agents.openai.session

# Prefer absolute import to match your new style:
from DGN_Agents.openai import OpenAISession, ChatGPTSession  # re-export

__all__ = ["OpenAISession", "ChatGPTSession"]
