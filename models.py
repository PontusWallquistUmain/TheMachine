from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File

class SongRequest(BaseModel):
    id: Optional[str] = None
    lyrics_type: Optional[str] = None
    lyrics_text: Optional[str] = None

    def set_id(self, id):
        if self.id is None:
            self.id = id
    
    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            "id": str(self.id),
            "audio": self.audio,
            "lyrics_type": self.lyrics_type,
            "lyrics_text": self.lyrics_text
        }

class SongResponse(BaseModel):
    id: str = None
    lead_vocals: Optional[str] = None
    instrumental: Optional[str] = None
    lyrics: Optional[str] = None

    def to_dict(self):
        return {
            "id": str(self.id),
            "lead_vocals": self.lead_vocals,
            "instrumental": self.instrumental,
            "lyrics": self.lyrics
        }

