# Turn: A single conversational step (morphism t → t+1)

from typing import Any, Dict, List, Optional, Literal
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field, model_validator

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class ContentPart(BaseModel):
    type: Literal["text", "json", "image", "file", "blob"]
    data: Optional[Any] = None
    uri: Optional[str] = None
    mime: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)

class Call(BaseModel):
    name: str
    args: Dict[str, Any] = Field(default_factory=dict)
    id: Optional[str] = None

class Turn(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    seq: Optional[int] = None  # assigned by Thread.append
    role: Literal["system", "user", "assistant", "tool", "function"]
    name: Optional[str] = None  # provider 'name' when relevant (e.g., function role)
    content: Optional[str] = None
    parts: Optional[List[ContentPart]] = None
    attachments: List[str] = Field(default_factory=list)
    content_type: Optional[Literal["text", "json", "parts", "binary"]] = None
    call: Optional[Call] = None
    received_at: datetime = Field(default_factory=now_utc)
    stop: Optional[str] = None
    tokens: Optional[Dict[str, int]] = None  # {"prompt","completion","total"}
    metadata: Dict[str, Any] = Field(default_factory=dict)
    provenance: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _validate_content_and_tokens(self):
        # Exactly one of content or parts
        has_content = self.content is not None
        has_parts = self.parts is not None
        if has_content == has_parts:
            raise ValueError("Exactly one of 'content' or 'parts' must be present.")

        # Token totals
        if self.tokens:
            p = int(self.tokens.get("prompt", 0))
            c = int(self.tokens.get("completion", 0))
            t = int(self.tokens.get("total", p + c))
            if t != p + c:
                raise ValueError("tokens.total must equal tokens.prompt + tokens.completion")
            # normalize
            self.tokens["total"] = t
        return self

    def __str__(self) -> str:
        return str(self.model_dump(exclude_none=True))
