from faster_whisper import WhisperModel
import time
import google.generativeai as genai

# ✅ Configure Gemini
genai.configure(api_key="AIza...")  # Replace with your actual key

# Load Whisper model
model = WhisperModel("medium", device="cuda", compute_type="float16")


def transcribe_audio(file_path):
    start = time.time()
    segments, info = model.transcribe(file_path, beam_size=5)
    transcript_text = " ".join([seg.text for seg in segments])
    print(f"🕒 Transcription took {time.time() - start:.2f} seconds")

    # 💾 Save transcript to file
    with open("static/transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print("✅ Transcript saved to transcript.txt")
    return transcript_text

    # generate_pdf(transcript_text) # Importing from pdfgen module
    # generate_qs(transcript_text) # Importing from pdfgen module
