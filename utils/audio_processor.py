import os
import shutil
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def configure_ffmpeg() -> str:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        ffmpeg_dir = os.getenv("FFMPEG_DIR")
        if ffmpeg_dir:
            ffmpeg = shutil.which("ffmpeg", path=ffmpeg_dir)
        if not ffmpeg:
            raise RuntimeError(
                "FFmpeg was not found. Install it and add its bin directory to PATH "
                "or set FFMPEG_DIR in .env."
            )
        os.environ["PATH"] = os.pathsep.join(
            filter(None, (os.path.dirname(os.path.abspath(ffmpeg)), os.environ.get("PATH")))
        )

    ffmpeg = os.path.abspath(ffmpeg)
    AudioSegment.converter = ffmpeg
    return os.path.dirname(ffmpeg)


def download_youtube_audio(url: str) -> str:
    ffmpeg_dir = configure_ffmpeg()
    output_path = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "ffmpeg_location": ffmpeg_dir,
        "no_color": True,
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # postprocessing ke baad final file hamesha <id>.wav hoti hai
        filename = os.path.join(DOWNLOAD_DIR, f"{info['id']}.wav")
    return filename


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to 16kHz mono WAV."""
    configure_ffmpeg()
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000
    base = os.path.splitext(wav_path)[0]

    chunks = []
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{base}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks


def process_input(source: str) -> list:
    if source.startswith(("http://", "https://")):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
        # Whisper ke liye 16kHz mono me convert
        wav_path = convert_to_wav(wav_path)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks