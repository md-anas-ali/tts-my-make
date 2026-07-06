import subprocess
import tempfile
import os
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()

class SpeechRequest(BaseModel):
    input: str
    voice: str = "en"
    response_format: str = "mp3"

@app.post("/v1/audio/speech")
async def tts(request: SpeechRequest):
    text = request.input
    voice = request.voice
    fmt = request.response_format.lower()

    if fmt not in ["mp3", "wav"]:
        return {"error": "Only mp3 or wav supported"}

    # Temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        wav_path = tmp_wav.name

    # Generate WAV using eSpeak NG
    subprocess.run([
        "espeak-ng",
        "-v", voice,
        text,
        "--stdout"
    ], stdout=open(wav_path, "wb"))

    if fmt == "wav":
        audio_bytes = open(wav_path, "rb").read()
        os.remove(wav_path)
        return Response(content=audio_bytes, media_type="audio/wav")

    # Convert WAV → MP3 using ffmpeg
    mp3_path = wav_path.replace(".wav", ".mp3")
    subprocess.run([
        "ffmpeg", "-y", "-i", wav_path, mp3_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    audio_bytes = open(mp3_path, "rb").read()
    os.remove(wav_path)
    os.remove(mp3_path)

    return Response(content=audio_bytes, media_type="audio/mpeg")        os.remove(wav_path)
        return Response(content=audio_bytes, media_type="audio/wav")

    # Convert WAV → MP3 using ffmpeg
    mp3_path = wav_path.replace(".wav", ".mp3")
    subprocess.run([
        "ffmpeg", "-y", "-i", wav_path, mp3_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    audio_bytes = open(mp3_path, "rb").read()
    os.remove(wav_path)
    os.remove(mp3_path)

    return Response(content=audio_bytes, media_type="audio/mpeg")
