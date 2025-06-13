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
        self.multi_cell(page_width, 12, title.upper(), align="C", fill=True)
        self.ln(8)
        self.set_text_color(0, 0, 0)        # Reset to black

    def write_heading(self, heading):
        self.set_fill_color(230, 230, 250)
        self.set_text_color(80, 0, 120)     # Purple
        self.set_font("DejaVu", "B", 13)
        self.multi_cell(0, 10, heading, fill=True)
        self.ln(3)
        self.set_text_color(0, 0, 0)
        self.set_font("DejaVu", size=12)

    def write_subheading(self, subheading):
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 8, subheading)
        self.ln(2)
        self.set_text_color(0, 0, 0)
        self.set_font("DejaVu", size=12)

    def write_content(self, line):
        self.set_font("DejaVu", size=12)
        self.multi_cell(0, 8, line)

def generate_pdf(transcript_text):
    #Enter your Google Gemini API key here
    genai.configure(api_key="Your_API_Key_Here")  # Replace with your actual key)
    gemini_model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")

    prompt = (
        "You are an expert academic note-taker. Given the following raw lecture transcript, generate "
        "clean, professional study notes in a style used at top universities. Use proper formatting with:\n"
        "- A title for the topic at the top\n"
        "- Clear section headings and subheadings\n"
        "- Bullet points or numbered lists for key ideas\n"
        "- Paragraphs only when needed\n"
        "- Do NOT use Markdown formatting like # or **\n\n"
        "If there is not enough information in the transcript, use your own knowledge to elaborate and fill in the gaps, "
        "Ensure the notes are highly formal, academic, and free from any casual, spoken, or lecture-style commentary such as "
        "'you know', 'uh', or any filler or informal expressions used by the lecturer.\n"
        "Rephrase everything into a polished, professional tone suitable for academic reference.\n\n"
        "If there is not enough information in the transcript, use your own knowledge to elaborate and fill in the gaps, "
        "ensuring the notes look complete, well-structured, and comprehensive for later studying.\n\n"
        "Transcript:\n"
        + transcript_text
    )

    start = time.time()
    response = gemini_model.generate_content(prompt)
    print(f"🕒 Notes generated in {time.time() - start:.2f} seconds")
    notes = response.text

    def text_to_pdf(text, output_file='static/notes.pdf'):
        pdf = StyledPDF()

        # Load fonts
        font_path_regular = "DejaVuSans.ttf"
        font_path_bold = "DejaVuSans-Bold.ttf"

        pdf.add_page()


        if not os.path.exists(font_path_regular) or not os.path.exists(font_path_bold):
            raise FileNotFoundError("❌ Font files not found in project directory.")

        pdf.add_font("DejaVu", "", font_path_regular, uni=True)
        pdf.add_font("DejaVu", "B", font_path_bold, uni=True)
        pdf.set_font("DejaVu", size=12)

        lines = text.strip().split('\n')

        # Detect title
        title = ""
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.isupper() and len(stripped.split()) <= 12:
                title = stripped
                lines = lines[i + 1:]
                break
            
        # fallback
        if not title:
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped:
                    title = stripped
                    lines = lines[i + 1:]
                    break

        if title:
            pdf.write_title(title)

        for line in lines:
            stripped = line.strip()
            if not stripped:
                pdf.ln(4)
            elif stripped.isupper():
                pdf.write_heading(stripped)
            elif stripped.endswith(":"):
                pdf.write_subheading(stripped)
            else:
                pdf.write_content(stripped)

        pdf.output(output_file)
        print("✅ Saved as notes.pdf")
        return title

    title = text_to_pdf(notes)
    return title


# Run
if __name__ == "__main__":
    with open("transcript.txt", "r", encoding="utf-8") as f:
        transcript_text = f.read()

    generate_pdf(transcript_text)
