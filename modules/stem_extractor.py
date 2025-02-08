import subprocess
import os
from utils.file_handler import get_output_intrumental_path
from utils.file_handler import get_output_no_vocals_path

def extract_stems(file_path, id):
    # Define the output directory
    output_dir = 'audio/output'
    os.makedirs(output_dir, exist_ok=True)

    # Run Demucs to separate the stems
    subprocess.run(['demucs', '--two-stems=vocals', '--mp3', '-o', output_dir, file_path], check=True)
    os.rename(get_output_no_vocals_path(id), get_output_intrumental_path(id))
