def get_input_path(id):
    return f"./audio/input/{id}.mp3"

def get_output_directory(id):
    return f"./audio/output/htdemucs/{id}"

def get_output_lyrics_path(id):
    return f"{get_output_directory(id)}/lyrics.mp3"

def get_output_intrumental_path(id):
    return f"{get_output_directory(id)}/instrumental.mp3"

def get_output_vocals_path(id):
    return f"{get_output_directory(id)}/vocals.mp3"
