from pydantic import BaseModel, conbytes
import uuid

class SongRequest(BaseModel):
    id: uuid.UUID
    audio: bytes
    lyricsType: str
    lyricsText: str

