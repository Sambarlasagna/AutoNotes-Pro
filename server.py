from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from audio_transcriber import transcribe_audio
import shutil

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/results", response_class=HTMLResponse)
async def read_results():
    with open("results.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("✅ File received")

    transcription = transcribe_audio(temp_path)
    print("✅ Transcription done")

    return {"message": "Audio uploaded and processing started"}

