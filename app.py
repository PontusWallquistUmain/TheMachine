from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Response, status
from models import SongRequest, SongResponse
from typing import Dict, List
from modules.transcriber import transcribe_lyrics
from modules.stem_extractor import extract_stems
from utils.file_handler import get_input_path
from utils.file_handler import get_output_lyrics_path
from utils.file_handler import get_output_intrumental_path
from utils.file_handler import get_output_vocals_path
import uuid
import os
import whisper
import threading

# Start the FastAPI app
app = FastAPI()

# Create a queue for storing the songs to be processed
song_queue: List[SongRequest] = []

# Initialize the cache to store the processed songs
song_cache: Dict[uuid.UUID, SongResponse] = {}

# Instantiate model
model = whisper.load_model("medium.en")

process_lock = threading.Lock()

@app.get("/")
def read_root():
    return {"message": "The Machine"}

@app.post("/queue/{id}")
async def add_to_karaoke_queue(
    response: Response,
    background_tasks: BackgroundTasks,
    id: uuid.UUID = None,
    lyrics_type: str = None,
    lyrics_text: str = None,
    audio: UploadFile = File(...)
    ):

    song_request = SongRequest(audio=audio, lyrics_type=lyrics_type, lyrics_text=lyrics_text)
    song_request.set_id(id)
    song_queue.append(song_request)

    audio_path = get_input_path(id)
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    background_tasks.add_task(process_song)
    if song_request in song_queue:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Song added to queue"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Error adding song to queue"}

@app.get("/cache/{id}", response_model=SongResponse)
def get_karaoke_song_if_ready(id: uuid.UUID, response: Response):
    if id in song_cache:
        return song_cache[id]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Song not ready"}

@app.get("/queue/", response_model=List[SongRequest])
def get_queue():
    return song_queue

@app.get("/cache/", response_model=Dict[uuid.UUID, SongResponse])
def get_cache():
    return song_cache

def process_song():
    with process_lock:
        while song_queue:
            song_request = song_queue.pop()

            audio_path = get_input_path(song_request.id)
            vocals_path = get_output_vocals_path(song_request.id)

            # Process the song
            print("Extracting stems...")
            extract_stems(audio_path)
            print("Stems extracted!")

            print("Transcribing lyrics...")
            transcribe_lyrics(vocals_path, song_request.get_id(), model)
            print("Lyrics transcribed!")

            # Save song to cache
            song_response = SongResponse(
                id=song_request.id,
                lead_vocals=get_output_vocals_path(song_request.id),
                instrumental=get_output_intrumental_path(song_request.id),
                lyrics=get_output_lyrics_path(song_request.id)
            )

            song_cache[song_request.id] = song_response
            print(f"Song {song_request.id} processed")
