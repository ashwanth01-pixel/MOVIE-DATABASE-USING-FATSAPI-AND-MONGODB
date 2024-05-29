from pydantic import BaseModel
from typing import Optional

class MovieCreate(BaseModel):
    title: str
    director: str
    release_year: int

class MovieUpdate(BaseModel):
    title: Optional[str]
    director: Optional[str]
    release_year: Optional[int]

class MovieResponse(MovieCreate):
    id: str
