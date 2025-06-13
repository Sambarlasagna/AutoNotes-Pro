# AutoNotes-Pro
AutoNotes-Pro is a FastAPI-based application that transcribes audio files, generates notes in PDF format, creates relevant questions, and even suggests additional resources.

---

## 🚀 Features

- Upload audio files and generate transcripts
- Automatically create:
  - 📄 Lecture Notes (PDF)
  - ❓ Questions based on content
  - 📚 External Resource links (PDF)
- Powered by:
  - Gemini API (for content generation)
  - YouTube Transcript API (if needed)
- Built using FastAPI and deployed with Uvicorn

---

## 📁 Project Structure
AutoNotes-Pro/

├── static/ # Contains index.html, results.html, and generated PDFs

├── server.py # Main FastAPI app

├── audio_transcriber.py # Handles transcription

├── pdfgen.py # Generates notes PDF

├── qsgen.py # Generates questions

├── res.py # Generates resources PDF



---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/AutoNotes-Pro.git
cd AutoNotes-Pro

python -m venv .venv
# Activate the environment:
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```
## Install Dependencies
```bash
pip install -r requirements.txt
```

## APIs Needed:-
- Youtube API
- Gemini API

## Run the APP:-
```bash
uvicorn server:app --reload
```

