from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Response, status
from fastapi.staticfiles import StaticFiles
from models import SongRequest, SongResponse
from typing import Dict, List
from modules.transcriber import transcribe_lyrics
from modules.stem_extractor import extract_stems
from utils.file_handler import get_input_path, get_output_lyrics_path, get_output_intrumental_path, get_output_vocals_path
from pathlib import Path
import os
import whisper
import asyncio
import uvicorn

app = FastAPI()

song_queue: List[SongRequest] = []
song_cache: Dict[str, SongResponse] = {}

def fill_song_cache():
    print("Filling song cache")
    base_directory = Path("./audio/output/htdemucs")
    for directory in base_directory.iterdir():
        if directory.is_dir():
            id = directory.name
            song_cache[id] = SongResponse(
                id=id,
                lead_vocals=get_output_vocals_path(id),
                instrumental=get_output_intrumental_path(id),
                lyrics=get_output_lyrics_path(id)
            )

fill_song_cache()
model = whisper.load_model("medium.en")

# Semaphore to ensure only one song is processed at a time
processing_semaphore = asyncio.Semaphore(1)

# Base directory for your audio files
base_directory = Path("./audio/output/htdemucs")

# Mount the directory containing your static files
app.mount("/static/", StaticFiles(directory=base_directory), name="static")

@app.get("/")
def read_root():
    return {"message": "The Machine"}

@app.post("/queue/{id}")
async def add_to_karaoke_queue(
    background_tasks: BackgroundTasks,
    response: Response,
    id: str = None,
    lyrics_type: str = None,
    lyrics_text: str = None,
    audio: UploadFile = File(...)
    ):

    if id in song_cache:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"message": "Song already in cache, request song from /cache/{id}"}

    song_request = SongRequest(audio=audio, lyrics_type=lyrics_type, lyrics_text=lyrics_text)
    song_request.set_id(id)
    song_queue.append(song_request)

    audio_path = get_input_path(id)
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    background_tasks.add_task(process_queue)

    if song_request in song_queue:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Song added to queue"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Error adding song to queue"}

@app.get("/cache/{id}")
def get_karaoke_song_if_ready(id: str, response: Response):
    if id in song_cache:
        return song_cache[id]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Song not ready"}

@app.get("/queue/", response_model=List[SongRequest])
def get_queue():
    return song_queue

@app.get("/cache/")
def get_cache():
    return song_cache

async def process_queue():
    async with processing_semaphore:
        while song_queue:
            song_request = song_queue[0]  # Get the first song in the queue
            await process_single_song(song_request)
            song_queue.pop(0)  # Remove the processed song from the queue

async def process_single_song(song_request: SongRequest):
    audio_path = get_input_path(song_request.id)
    vocals_path = get_output_vocals_path(song_request.id)

    print("Extracting stems...")
    await asyncio.to_thread(extract_stems, audio_path, song_request.get_id())
    print("Stems extracted!")

    print("Transcribing lyrics...")
    await asyncio.to_thread(transcribe_lyrics, vocals_path, song_request.get_id(), model)
    print("Lyrics transcribed!")

    song_response = SongResponse(
        id=song_request.id,
        lead_vocals=get_output_vocals_path(song_request.id),
        instrumental=get_output_intrumental_path(song_request.id),
        lyrics=get_output_lyrics_path(song_request.id)
    )

    song_cache[song_request.id] = song_response
    print(f"Song {song_request.id} processed")

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=False)