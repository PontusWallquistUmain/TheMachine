import whisper
import time

model_name = "medium.en"
model = whisper.load_model(model_name)

def transcribe_lyrics(file_path):
    return model.transcribe(file_path, fp16=False)
    
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:05.2f}"

if __name__ == "__main__":
    start = time.time()
    result = transcribe_lyrics("audio/output/htdemucs/audio/vocals.mp3")
    end = time.time()
    print(f"Model: {model_name}\nTime: {end-start}")
    for segment in result['segments']:
        start = format_timestamp(segment["start"])
        text = segment["text"]
        print(f"start_time: [{start}] {text}")
