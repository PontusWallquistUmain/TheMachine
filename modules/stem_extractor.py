import subprocess
import os

def extract_stems(file_path):
    # Define the output directory
    output_dir = 'audio/output'
    os.makedirs(output_dir, exist_ok=True)

    # Run Demucs to separate the stems
    subprocess.run(['demucs', '--two-stems=vocals', '--mp3', '-o', output_dir, file_path], check=True)
