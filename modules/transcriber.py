import whisper
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import time

model_name = "medium.en"
model = whisper.load_model(model_name)
    
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:05.2f}"

def detect_start(audio):
    non_silent_segments = detect_nonsilent(audio, 1000, -40)
    return non_silent_segments[0][0] if non_silent_segments else 0


def write_to_lrc(transcription, file_path, uuid_str):
    output_path = file_path[:file_path.rfind('/')] + "/lyrics.lrc"

    # Detect start of first lyric segment
    audio = AudioSegment.from_file(file_path)
    detected_start = detect_start(audio)

    first_iter = True
    with open(output_path, "w", encoding="utf-8") as lrc_file:
        for segment in transcription['segments']:
            if first_iter:
                start_time = format_timestamp(detected_start/1000)
                first_iter = False
            else:
                start_time = format_timestamp(segment['start'])
                
            text = segment['text'].strip()
            lrc_file.write(f"[{start_time}]{text}\n")

def transcribe_lyrics(file_path, uuid_str):
    result = model.transcribe(file_path, fp16=False)
    write_to_lrc(result, file_path, uuid_str)

# if __name__ == "__main__":
#     start = time.time()
#     result = transcribe_lyrics("audio/output/htdemucs/audio/vocals.mp3")
#     end = time.time()
#     print(f"Model: {model_name}\nTime: {end-start}")
