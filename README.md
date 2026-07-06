# eSpeak NG TTS API

A lightweight FastAPI-based Text-to-Speech API using eSpeak NG.  
Runs on Render Free (512 MB RAM, 0.1 CPU).

## Endpoint
POST /v1/audio/speech

### Request Body
```json
{
  "input": "Hello world",
  "voice": "en",
  "response_format": "mp3"
}
