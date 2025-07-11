# Jarvis

Personal Jarvis assistant project.

---

## ✅ Completed

- Local audio recording and transcription using Whisper works correctly.
- Integrated Ollama LLM model (`phi3:mini`) for text-based responses.
- Added text-to-speech output with English (US) voice using `pyttsx3`.
- Automatic model installation if missing.
- Dynamic hearing with background sound and time threshold.
- Clean flow: speech input → LLM response → spoken output.

---

## 🚀 Next Steps

- Add wake word detection with [pvporcupine](https://github.com/Picovoice/porcupine) for hands-free activation.
- Potentially add conversational context and continuous dialogue.

---

## 📦 Installation & Requirements

- Python dependencies listed in `requirements.txt` are mandatory.
- Requires `ffmpeg` installed and accessible on the system for Whisper audio processing.
- Ollama CLI installed and configured (ensure it’s in the system PATH).
- Windows users: voice setup defaults to **Microsoft Zira Desktop** English voice for TTS.

---

If you want, I can help you generate a polished `requirements.txt` or setup guide next!
