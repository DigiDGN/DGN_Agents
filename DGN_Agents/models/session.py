# Thread: An append-only transcript of Turns (dialogue state)
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from .message import Turn
from .provider import ModelCfg

class Thread(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    title: Optional[str] = None
    system: str
    model_cfg: ModelCfg
    wire_fields: Set[str] = Field(default_factory=set)
    turns: List["Turn"] = Field(default_factory=list)
    window: Optional[int] = None
    keep: bool = True
    totals: Dict[str, Dict[str, int]] = Field(default_factory=lambda: {"tokens": {"prompt": 0, "completion": 0, "total": 0}})
    schema_version: int = 1

    def append(self, turn: "Turn"):
        turn.seq = len(self.turns) + 1
        if not turn.received_at:
            turn.received_at = datetime.now(timezone.utc)
        if turn.tokens:
            for k in ("prompt", "completion", "total"):
                self.totals["tokens"][k] += turn.tokens.get(k, 0)
        self.turns.append(turn)

    def format_for_provider(self, system_turn: "Turn", user_turn: "Turn") -> List[Dict[str, Any]]:
        recent = self.turns[-self.window:] if self.window else self.turns
        def to_wire(t: "Turn"):
            return t.model_dump(include=self.wire_fields, exclude_none=True)
        return [to_wire(system_turn)] + [to_wire(t) for t in recent] + [to_wire(user_turn)]

    def __str__(self):
        started = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        n = len(self.turns)
        last = self.turns[-1].received_at.strftime("%Y-%m-%d %H:%M:%S") if self.turns else "N/A"
        return f"Thread started at {started}:\n  - {n:,} Turns\n  - Last turn at {last}"
