## System Requirements

This project requires several system-level dependencies to be installed for audio processing. Please ensure the following are installed on your system:

### FFmpeg

FFmpeg is used for handling various audio and video formats. It is a prerequisite for running the audio extraction functionality.

#### Installation Instructions

- **macOS:** Use Homebrew to install FFmpeg:
  brew install ffmpeg

- **Linux:** Use your distribution's package manager. For example, on Ubuntu:
  sudo apt update
  sudo apt install ffmpeg

- **Windows:** Download FFmpeg from the [official website](https://ffmpeg.org/download.html) or use Chocolatey:
  choco install ffmpeg

### SoX

SoX is a cross-platform command-line audio processing tool. It is required for `torchaudio` to function correctly.

#### Installation Instructions

- **macOS:** Use Homebrew to install SoX:
  brew install sox

- **Linux:** Use your distribution's package manager. For example, on Ubuntu:
  sudo apt update
  sudo apt install sox

- **Windows:** Download the Windows binaries from the [SoX website](http://sox.sourceforge.net/).

### libsndfile

`libsndfile` is a library for reading and writing files containing sampled sound. It is required for `torchaudio` to function correctly.

#### Installation Instructions

- **macOS:** Use Homebrew to install libsndfile:
  brew install libsndfile

- **Linux:** Use your distribution's package manager. For example, on Ubuntu:
  sudo apt update
  sudo apt install libsndfile1

- **Windows:** You may need to compile it from source or find a precompiled binary.


## Installation
To install the dependencies, run:
```bash
pip install -r requirements.txt
```

## Running the server
To start the server, run:
```bash
python3 -m uvicorn app:app --reload
```
