from fastapi import FastAPI
from models import SongRequest, SongResponse
from typing import Dict, List
import uuid

# Start the FastAPI app
app = FastAPI()

# Create a queue for storing the songs to be processed
song_queue: List[SongRequest] = []

# Initialize the cache to store the processed songs
song_cache: Dict[uuid.UUID, SongResponse] = {}

@app.get("/")
def read_root():
    return {"message": "The Machine"}

@app.post("/queue/{id}")
def add_to_karaoke_queue(song_request: SongRequest):
    song_request.set_id(id)
    song_queue.append(song_request)
    if song_request in song_queue:
        return {"message": "Song added to queue"}
    else:
        return {"error": "Error adding song to queue"}

@app.get("/cache/{id}", response_model=SongResponse)
def get_karaoke_song_if_ready(id: uuid.UUID):
    if id in song_cache:
        return song_cache[id]
    else:
        return {"message": "Song not ready"}

@app.get("/queue/", response_model=List[SongRequest])
def get_queue():
    return song_queue

@app.get("/cache/", response_model=Dict[uuid.UUID, SongResponse])
def get_cache():
    return song_cache