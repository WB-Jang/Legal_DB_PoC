from __future__ import annotations
from typing import Literal, Dict, Any
from pydantic import BaseModel
from functools import lru_cache

class AgentState(BaseModel):
    user_input: str
    keywords: list[Any]|None=None
    result: list[Any]|None=None
    rank: int
    rerank: int
    final_answer : list[Any]|None=None