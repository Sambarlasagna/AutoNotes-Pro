from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

from audio_transcriber import transcribe_audio
from pdfgen import generate_pdf
from qsgen import generate_qs
from res import resource_pdf_gen

app = FastAPI()

# Serve the 'static' directory at the '/static' route
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    # Redirect to static/index.html
    return RedirectResponse(url="/static/index.html")

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("✅ File received")

    # Transcribe and generate all outputs
    # transcript = transcribe_audio(temp_path)
    # print("✅ Transcription done")
    with open("static/transcript.txt", "r") as f:
        transcript = f.read()

    title = generate_pdf(transcript)
    print("✅ PDF done")

    generate_qs(transcript)
    print("✅ Questions done")

    resource_pdf_gen(title)
    print("✅ Resources done")

    # Clean up temp file
    os.remove(temp_path)

    if os.path.exists("DejavuSans.pkl"):
        os.remove("DejavuSans.pkl")
        print(f"Deleted DejavuSans.pkl file")
    else:
        print("File does not exist")

    if os.path.exists("DejavuSans.cw127.pkl"):
        os.remove("DejavuSans.cw127.pkl")
        print(f"Deleted DejavuSans.cw127pkl file")
    else:
        print("File does not exist")

    if os.path.exists("DejavuSans-Bold.pkl"):
        os.remove("DejavuSans-Bold.pkl")
        print(f"Deleted DejavuSans-Bold.pkl file")
    else:
        print("File does not exist")

    if os.path.exists("DejavuSans-Bold.cw127.pkl"):
        os.remove("DejavuSans.cw127.pkl")
        print(f"Deleted DejavuSans.cw127 file")
    else:
        print("File does not exist")

    return {"status": "done", "redirect": "/static/results.html"}

