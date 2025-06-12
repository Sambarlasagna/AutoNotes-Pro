from faster_whisper import WhisperModel
import time
from pdfgen import generate_pdf  
from pdfgen import generate_qs

# ✅ Configure Gemini
genai.configure(api_key="AIza...")  # Replace with your actual key

# Load Whisper model
model = WhisperModel("medium", device="cuda", compute_type="float16")

def text_to_pdf(text, output_file='notes.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line.strip() or " ")

    pdf.output(output_file)

def transcribe_audio(file_path):
    start = time.time()
    segments, info = model.transcribe(file_path, beam_size=5)
    transcript_text = " ".join([seg.text for seg in segments])
    print(f"🕒 Transcription took {time.time() - start:.2f} seconds")

    # 💾 Save transcript to file
    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print("✅ Transcript saved to transcript.txt")

    generate_pdf(transcript_text) # Importing from pdfgen module
    generate_qs(transcript_text) # Importing from pdfgen module
