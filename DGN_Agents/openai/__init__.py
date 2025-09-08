from .session import OpenAISession
ChatGPTSession = OpenAISession  # back-compat

__all__ = ["OpenAISession", "ChatGPTSession"]
