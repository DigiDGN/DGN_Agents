# Turn: A single conversational step (morphism t → t+1)
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class ContentPart(BaseModel):
    type: str  # "text"|"json"|"image"|"file"|"blob"
    data: Optional[Any] = None
    uri: Optional[str] = None
    mime: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

class Turn(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    seq: int
    role: str  # "system"|"user"|"assistant"|"tool"
    content: Optional[str] = None
    parts: Optional[List[ContentPart]] = None
    attachments: Optional[List[str]] = None
    content_type: Optional[str] = None  # "text"|"json"|"parts"|"binary"
    call: Optional[Dict[str, Any]] = None  # { name: str, args: dict, id?: str }
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    stop: Optional[str] = None
    tokens: Optional[Dict[str, int]] = None  # { prompt?: int, completion?: int, total?: int }
    metadata: Dict[str, Any] = Field(default_factory=dict)
    provenance: Dict[str, Any] = Field(default_factory=dict)

    def __post_init_post_parse__(self):
        if (self.content is None) == (self.parts is None):
            raise ValueError("Exactly one of 'content' or 'parts' must be present.")
        if self.tokens:
            prompt = self.tokens.get("prompt", 0)
            completion = self.tokens.get("completion", 0)
            total = self.tokens.get("total", 0)
            if total != prompt + completion:
                raise ValueError("tokens.total must equal tokens.prompt + tokens.completion")
