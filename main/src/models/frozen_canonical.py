from typing import Optional, Literal
from pydantic import BaseModel, Field


class PathIDs(BaseModel):
    act: str
    chapter: Optional[str] = None
    section: Optional[str] = None
    subsection: Optional[str] = None
    clause: Optional[str] = None


class PathTitles(BaseModel):
    act: str
    chapter: Optional[str] = None
    section: Optional[str] = None
    subsection: Optional[str] = None
    clause: Optional[str] = None


class RetrievalUnit(BaseModel):
    id: str = Field(..., description="Stable deterministic ID")
    type: Literal["clause", "subsection", "section"]

    text: str = Field(..., min_length=10)

    path_ids: PathIDs
    path_titles: PathTitles

    language: Literal["ne"] = "ne"

    class Config:
        frozen = True

class RetrievedUnit(BaseModel):
    id: str
    type: Literal["clause", "subsection", "section"]
    text: str

    act: str
    chapter: Optional[str] = None
    section: Optional[str] = None
    subsection: Optional[str] = None
    clause: Optional[str] = None

    language: Literal["ne"] = "ne"
