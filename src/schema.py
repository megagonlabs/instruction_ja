#!/usr/bin/env python3

from typing import Any, Literal, Optional

from pydantic import BaseModel


class Utterance(BaseModel):
    name: Literal["user", "agent"]
    text: str


class Source(BaseModel):
    path: str
    line_index: int


class OriginalInfo(BaseModel):
    sources: list[Source]
    utterances: dict[str, list[Utterance]]


class Example(BaseModel):
    id: str
    utterances: list[Utterance]
    original_info: Optional[OriginalInfo] = None
    meta: dict[str, Any] = {}
