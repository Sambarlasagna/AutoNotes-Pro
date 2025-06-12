import streamlit as st
import tempfile
from audio_transcriber import transcribe_audio_file

st.set_page_config(page_title="AutoNotes Pro", page_icon="📚")
st.title("AutoNotes Pro 📚")

st.markdown("Upload your **audio lecture file** below:")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file:
    if st.button("Generate Study Pack 🚀"):
        with st.spinner("Transcribing..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            transcript = transcribe_audio_file(tmp_path)

            if transcript:
                st.success("Study Pack generated successfully! 📚")
                st.markdown("### Transcript:")
                st.text(transcript)
            else:
                st.error("Failed to generate transcript. Try another audio file.")
