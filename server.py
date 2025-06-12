from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import shutil

from audio_transcriber import transcribe_audio
from pdfgen import generate_pdf
from qsgen import generate_qs
from res import resource_pdf_gen

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
    
    # Save the uploaded file
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("✅ File received")

    # Step 1: Transcribe
    transcript = transcribe_audio(temp_path)
    print("✅ Transcription done")

    # Step 2: Generate PDF
    title = generate_pdf(transcript)
    print("✅ PDF done")

    # Step 3: Generate Questions
    generate_qs(transcript)
    print("✅ Questions done")

    # Step 4: Generate Resources
    resource_pdf_gen(title)
    print("✅ Resources done")

    # Step 5: Redirect to results
    return RedirectResponse(url="/results", status_code=303)
