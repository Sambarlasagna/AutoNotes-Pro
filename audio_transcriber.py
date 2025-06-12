# audio_transcriber.py
from faster_whisper import WhisperModel
from ollama import Client
from fpdf import FPDF
import time

# Load model once
model = WhisperModel("medium", device="cuda", compute_type="float16")

def text_to_pdf(text, output_file='notes.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split('\n'):
        if line.strip() == "":
            pdf.ln()
        else:
            pdf.multi_cell(0, 10, line)

    pdf.output(output_file)

def transcribe_audio(file_path):
    print("[INFO] Starting transcription...")
    start = time.time()

    segments, info = model.transcribe(file_path)
    transcript_text = ""
    for segment in segments:
        transcript_text += f"{segment.text.strip()}\n"

    end = time.time()
    print(f"[INFO] Transcription took {end - start:.2f} seconds")

    print("[INFO] Sending transcript to Ollama...")
    start = time.time()

    client = Client(host='http://localhost:11434')
    response = client.chat(
        model='llama3',
        messages=[
            {"role": "system", "content": "You are an expert at converting transcripts into structured study notes."},
            {"role": "user", "content": "Convert the following transcript into clean notes with headings and bullet points:\n\n" + transcript_text}
        ]
    )

    end = time.time()
    print(f"[INFO] Chat response took {end - start:.2f} seconds")

    notes = response['message']['content']
    print("[INFO] Notes generated successfully.")

    text_to_pdf(notes, 'notes.pdf')
    print("[INFO] Notes saved to notes.pdf")

# Example usage:
# transcribe_audio("temp_thermodynamics_1hr.mp3")