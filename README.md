# AI Video Assistant

AI Video Assistant turns YouTube videos and local audio or video files into searchable meeting notes. Use the Streamlit interface to run the pipeline and ask questions about a transcript.

## Features

- Accepts a YouTube URL or a local media file path accessible to the app.
- Transcribes audio locally with Whisper in English mode. Hinglish mode uses Sarvam to produce an English transcript.
- Uses Mistral to generate a meeting title and summary and extract action items, key decisions, and open questions.
- Uses retrieval-augmented generation (RAG) to answer questions using relevant transcript excerpts retrieved from Chroma.

## Setup

1. Install Python 3.12 and FFmpeg, including `ffprobe`. Put FFmpeg's `bin` directory on `PATH` or set `FFMPEG_DIR` to that directory in `.env`.
2. From the project directory, create a virtual environment and install the dependencies.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

   On macOS or Linux, activate the environment with `source .venv/bin/activate`.
3. Copy `.env.example` to `.env` and replace `your_key_here` with your Mistral API key. Leave `FFMPEG_DIR` empty if FFmpeg is on `PATH`. Add `SARVAM_API_KEY` if you plan to use Hinglish mode.
4. Start the app.

   ```sh
   streamlit run app.py
   ```

5. Enter a YouTube URL or a local file path in the sidebar, choose a language, and click **Analyse**. The first run can download the Whisper and embedding models.
