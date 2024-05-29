from fastapi import FastAPI, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from models import Movie
from schemas import MovieCreate, MovieResponse, MovieUpdate
from bson import ObjectId
from pydantic import BaseModel

app = FastAPI()

# Database connection
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.movie_database

@app.post("/movies/", response_model=MovieResponse)
async def create_movie(movie: MovieCreate):
    movie_dict = movie.dict()
    result = await db.movies.insert_one(movie_dict)
    if result.inserted_id:
        return MovieResponse(**movie_dict, id=str(result.inserted_id))
    raise HTTPException(status_code=500, detail="Movie could not be added")

@app.get("/movies/", response_model=List[MovieResponse])
async def get_movies():
    movies = await db.movies.find().to_list(1000)
    return [MovieResponse(**movie, id=str(movie["_id"])) for movie in movies]

@app.put("/movies/{movie_id}", response_model=MovieResponse)
async def update_movie(movie_id: str, movie: MovieUpdate):
    result = await db.movies.update_one({"_id": ObjectId(movie_id)}, {"$set": movie.dict(exclude_unset=True)})
    if result.modified_count:
        updated_movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
        return MovieResponse(**updated_movie, id=str(updated_movie["_id"]))
    raise HTTPException(status_code=404, detail="Movie not found")

@app.delete("/movies/{movie_id}", response_model=BaseModel)
async def delete_movie(movie_id: str):
    result = await db.movies.delete_one({"_id": ObjectId(movie_id)})
    if result.deleted_count:
        return {"detail": "Movie deleted successfully"}
    raise HTTPException(status_code=404, detail="Movie not found")
