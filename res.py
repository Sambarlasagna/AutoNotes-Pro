from fpdf import FPDF
import requests

def resource_pdf_gen(topic_title):
    # Enter your YouTube API Key here
    YOUTUBE_API_KEY = "API_KEY_HERE"

    font_path_regular = "DejaVuSans.ttf"
    font_path_bold = "DejaVuSans-Bold.ttf"

    def search_youtube_videos(query, max_results=3):
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "key": YOUTUBE_API_KEY,
        }
        response = requests.get(url, params=params)
        videos = []
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                title = item["snippet"]["title"]
                video_id = item["id"]["videoId"]
                link = f"https://www.youtube.com/watch?v={video_id}"
                videos.append((title, link))
        else:
            print("❌ YouTube API Error:", response.text)
        return videos

    def generate_resources_pdf(output_file="static/resources.pdf"):
        pdf = FPDF()
        pdf.add_font("DejaVu", "", font_path_regular, uni=True)
        pdf.add_font("DejaVu", "B", font_path_bold, uni=True)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Header
        pdf.set_fill_color(230, 230, 250)
        pdf.set_font("DejaVu", "B", 16)
        pdf.cell(0, 12, "Supplementary Resources", ln=True, align="C", fill=True)
        pdf.ln(8)

        # Topic
        pdf.set_font("DejaVu", "B", 13)
        pdf.cell(0, 10, f"Topic: {topic_title}", ln=True)
        pdf.ln(6)

        # YouTube Videos
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "1. YouTube Videos", ln=True)
        pdf.set_font("DejaVu", "", 11)

        videos = search_youtube_videos(topic_title)
        if videos:
            for i, (title, link) in enumerate(videos, 1):
                pdf.multi_cell(0, 8, f"{i}. {title}")
                pdf.set_text_color(0, 0, 255)
                pdf.set_font("DejaVu", "U", 11)
                pdf.cell(0, 8, link, ln=True, link=link)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("DejaVu", "", 11)
                pdf.ln(2)
        else:
            pdf.cell(0, 8, "No videos found.")
        pdf.ln(6)

        # Recommended Websites
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "2. Recommended Websites", ln=True)
        pdf.set_font("DejaVu", "U", 11)
        pdf.set_text_color(0, 0, 255)
        websites = [
            "https://www.khanacademy.org/",
            "https://nptel.ac.in/",
            "https://ocw.mit.edu/"
        ]
        for site in websites:
            pdf.cell(0, 8, site, ln=True, link=site)
        pdf.set_text_color(0, 0, 0)

        # Save PDF
        pdf.output(output_file)
        print(f"✅ Saved resources to {output_file}")

    generate_resources_pdf()

if __name__ == "__main__":
    sample_topic = "Laws of Thermodynamics"
    resource_pdf_gen(sample_topic)
