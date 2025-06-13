from fpdf import FPDF
import google.generativeai as genai
import time
import os

class StyledPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def write_title(self, title):
        self.set_fill_color(230, 230, 250)  # Light lavender
        self.set_text_color(0, 0, 128)      # Dark blue
        self.set_font("DejaVu", "B", 15)
        page_width = self.w - 2 * self.l_margin
        self.set_x(self.l_margin)
        self.multi_cell(page_width, 12, title, align="C", fill=True)
        self.ln(8)
        self.set_text_color(0, 0, 0)

    def write_question(self, question):
        self.set_font("DejaVu", "B", 12)
        self.multi_cell(0, 8, question)

    def write_answer(self, answer):
        self.set_font("DejaVu", size=12)
        self.multi_cell(0, 8, answer)
        self.ln(6)

def generate_qs(transcript_text):
    #Enter your Google Gemini API key here
    genai.configure(api_key="Your_API_Key_Here")  # Replace with your actual key
    gemini_model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")

    prompt = (
        "You are an expert academic question generator. Based on the transcript below, generate a lecture-based questionnaire "
        "with at least 8 to 10 questions. Use a mix of:\n"
        "- Multiple Choice Questions (MCQs) with 4 options (a, b, c, d)\n"
        "- Short one-line answer questions\n\n"
        "Instructions:\n"
        "- Start each question with a number like 1. 2. etc.\n"
        "- After each question, write 'Answer: ...' clearly on the next line\n"
        "- Do NOT use markdown formatting (#, **, etc.)\n"
        "- Keep the layout clean and easy to read.\n\n"
        "Transcript:\n"
        + transcript_text
    )

    start = time.time()
    response = gemini_model.generate_content(prompt)
    print(f"🕒 Questions generated in {time.time() - start:.2f} seconds")
    questionnaire = response.text

    def text_to_pdf(text, output_file='static/questionnaire.pdf'):
        pdf = StyledPDF()
        pdf.add_page()

        # Load fonts
        font_path_regular = "DejaVuSans.ttf"
        font_path_bold = "DejaVuSans-Bold.ttf"

        if not os.path.exists(font_path_regular) or not os.path.exists(font_path_bold):
            raise FileNotFoundError("❌ Font files not found in project directory.")

        pdf.add_font("DejaVu", "", font_path_regular, uni=True)
        pdf.add_font("DejaVu", "B", font_path_bold, uni=True)
        pdf.set_font("DejaVu", size=12)

        # Title
        pdf.write_title("Lecture-Based Questionnaire")

        # Process Q&A
        lines = text.strip().split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            if line[0].isdigit() and line[1] == '.':
                pdf.write_question(line)
                if i + 1 < len(lines) and lines[i + 1].strip().lower().startswith("answer"):
                    i += 1
                    pdf.write_answer(lines[i].strip())
                else:
                    pdf.ln(6)
            else:
                pdf.multi_cell(0, 8, line)
            i += 1

        pdf.output(output_file)
        print(f"✅ Saved as {output_file}")

    text_to_pdf(questionnaire)

# Load transcript and run
if __name__ == "__main__":
    with open("transcript.txt", "r", encoding="utf-8") as f:
        transcript_text = f.read()

    generate_qs(transcript_text)
