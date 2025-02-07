from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from models import SongRequest, SongResponse
from typing import Dict, List
from modules.transcriber import transcribe_lyrics
from modules.stem_extractor import extract_stems
import uuid
import os

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
async def add_to_karaoke_queue(background_tasks: BackgroundTasks, id: uuid.UUID, lyrics_type: str = None, lyrics_text: str = None, audio: UploadFile = File(...)):
    song_request = SongRequest(audio=audio, lyrics_type=lyrics_type, lyrics_text=lyrics_text)
    song_request.set_id(id)
    song_queue.append(song_request)

    audio_path = f"./audio/input/{id}.mp3"
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    background_tasks.add_task(process_song)
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

def process_song():
    while song_queue:
        song_request = song_queue.pop()

        audio_path = f"/audio/input/{song_request.id}.mp3"

        # Process the song
        extract_stems(audio_path)
        transcribe_lyrics(audio_path)

        # Save song to cache
        song_response = SongResponse(
            id=song_request.id,
            lead_vocals="Processed lead vocals",
            instrumental="Processed instrumental",
            lyrics=song_request.lyrics_text
        )
        song_cache[song_request.id] = song_response
        print(f"Song {song_request.id} processed")