# Provider configuration for model endpoints
from typing import Any, Dict
from pydantic import BaseModel, Field, HttpUrl, SecretStr

class ModelCfg(BaseModel):
    api_url: HttpUrl
    name: str
    auth: Dict[str, SecretStr] = Field(default_factory=dict)
    params: Dict[str, Any] = Field(default_factory=dict)
