import whisper
import time

model_name = "medium.en"
model = whisper.load_model(model_name)
    
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:05.2f}"

def write_to_lrc(transcription, file_path):
    output_path = file_path[:file_path.rfind('/')] + ".lrc"

    with open(output_path, "w", encoding="utf-8") as lrc_file:
        for segment in transcription['segments']:
            start_time = format_timestamp(segment['start'])
            text = segment['text'].strip()
            lrc_file.write(f"[{start_time}]{text}\n")

def transcribe_lyrics(file_path):
    result = model.transcribe(file_path, fp16=False)
    write_to_lrc(result, file_path)

# if __name__ == "__main__":
#     start = time.time()
#     result = transcribe_lyrics("audio/output/htdemucs/audio/vocals.mp3")
#     end = time.time()
#     print(f"Model: {model_name}\nTime: {end-start}")
