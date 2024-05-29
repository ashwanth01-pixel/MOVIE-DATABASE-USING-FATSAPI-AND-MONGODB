from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    director: str
    release_year: int
