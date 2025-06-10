import streamlit as st

st.title("AutoNotes Pro 📚")
audio = st.file_uploader("Upload your lecture audio", type=["mp3", "wav"])

if audio is not None:
    st.audio(audio, format='audio/wav')
    if st.button("Generate Study Pack 🚀"):
        with st.spinner("Transcribing..."):
            # transcribe via whisper
            pass
        st.success("Done!")
        st.markdown("### 📝 Title: The French Revolution")
        st.markdown("### 🗒️ Notes:")
        st.markdown("• ...")
        st.download_button("Download PDF", data="...", file_name="notes.pdf")
