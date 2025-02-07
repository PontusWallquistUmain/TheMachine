import whisper

model = whisper.load_model("turbo")

def transcribe_lyrics(file_path):
    return model.transcribe(file_path, fp16=False)

if __name__ == "__main__":
    #result = transcribe_lyrics("audio/input/audio.mp3")
    result = transcribe_lyrics("audio/output/htdemucs/audio/vocals.mp3")
    print(result["text"])
