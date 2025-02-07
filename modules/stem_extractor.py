import subprocess
import os
import torchaudio

def extract_stems(file_path):
    # Set Audio Backend
    #torchaudio.set_audio_backend('sox')

    # Define the output directory
    output_dir = 'audio/output'
    os.makedirs(output_dir, exist_ok=True)

    # Run Demucs to separate the stems
    subprocess.run(['demucs', '--two-stems=vocals', '--mp3', '-o', output_dir, file_path], check=True)



# if __name__ == "__main__":
#     #print("Available backends:", torchaudio.list_audio_backends())
#     extract_stems('audio/input/audio.mp3')
