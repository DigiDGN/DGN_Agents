# models/session.py
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from .message import Turn
from .provider import ModelCfg

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def _zero_totals() -> Dict[str, Dict[str, int]]:
    return {"tokens": {"prompt": 0, "completion": 0, "total": 0}}

class Thread(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=now_utc)
    title: Optional[str] = None

    system: str
    model_cfg: ModelCfg
    wire_fields: Set[str] = Field(default_factory=set)  # e.g. {"role","content","name"}

    turns: List[Turn] = Field(default_factory=list)
    window: Optional[int] = None
    keep: bool = True

    totals: Dict[str, Dict[str, int]] = Field(default_factory=_zero_totals)
    schema_version: int = 1

    # --- Back-compat fields for current repo (remove after chatgpt.py is refactored) ---
    auth: Optional[Dict[str, Any]] = None
    api_url: Optional[str] = None
    model: Optional[str] = None
    params: Dict[str, Any] = Field(default_factory=dict)

    # legacy token counters (chatgpt.py increments these directly today)
    total_prompt_length: int = 0
    total_completion_length: int = 0
    total_length: int = 0

    def append(self, turn: Turn) -> None:
        # assign seq
        turn.seq = (self.turns[-1].seq + 1) if self.turns else 1

        # normalize timestamp to UTC if tz-naive
        dt = turn.received_at
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            turn.received_at = dt.replace(tzinfo=timezone.utc)

        # append
        self.turns.append(turn)

        # roll up tokens (supports both new tokens dict and legacy fields)
        if turn.tokens:
            p = int(turn.tokens.get("prompt", 0))
            c = int(turn.tokens.get("completion", 0))
            t = int(turn.tokens.get("total", p + c))
        else:
            p = int(getattr(turn, "prompt_length", 0) or 0)
            c = int(getattr(turn, "completion_length", 0) or 0)
            t = int(getattr(turn, "total_length", p + c) or (p + c))

        self.totals["tokens"]["prompt"] += p
        self.totals["tokens"]["completion"] += c
        self.totals["tokens"]["total"] += t

        # keep legacy counters in sync
        self.total_prompt_length += p
        self.total_completion_length += c
        self.total_length += t

    def format_for_provider(self, system_turn: Turn, user_turn: Turn) -> List[Dict[str, Any]]:
        history = self.turns[-self.window:] if self.window else self.turns
        chain = [system_turn, *history, user_turn]

        # default wire_fields if not set (OpenAI-like)
        fields = self.wire_fields or {"role", "content", "name"}

        out: List[Dict[str, Any]] = []
        for t in chain:
            msg = t.model_dump(include=fields, exclude_none=True)
            out.append(msg)
        return out

    def format_input_messages(self, system_message: Turn, user_message: Turn) -> List[Dict[str, Any]]:
        """Back-compat shim: delegate to format_for_provider."""
        return self.format_for_provider(system_message, user_message)

    def add_messages(
        self,
        user_message: Turn,
        assistant_message: Turn,
        save_messages: Optional[bool] = None,
    ) -> None:
        """Back-compat shim: mimic original save_messages semantics."""
        to_save = isinstance(save_messages, bool)
        if to_save:
            do_save = save_messages
        else:
            do_save = self.keep  # renamed from save_messages -> keep
        if do_save:
            self.append(user_message)
            self.append(assistant_message)

    def __str__(self) -> str:
        started = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if self.turns:
            last = self.turns[-1].received_at.strftime("%Y-%m-%d %H:%M:%S")
            return f"Thread started at {started}:\n  - {len(self.turns):,} Turns\n  - Last turn at {last}"
        return f"Thread started at {started}:\n  - 0 Turns"
