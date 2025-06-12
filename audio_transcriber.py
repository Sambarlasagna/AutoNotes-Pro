from transformers import pipeline
import torch
import torchaudio

# Load model once globally
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-base")

def transcribe_audio_file(audio_path):
    try:
        # Load and resample audio
        speech_array, sampling_rate = torchaudio.load(audio_path)
        resampler = torchaudio.transforms.Resample(orig_freq=sampling_rate, new_freq=16000)
        speech = resampler(speech_array).squeeze().numpy()

        result = pipe(speech)
        return result.get("text", "")
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

