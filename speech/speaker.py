import pyttsx3


def speak(text):
    """
    Function to speak a text
    Args:
        text (str): text to speak
    """
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    target_voice_name = "Microsoft Zira Desktop - English (United States)"

    for voice in voices:
        if target_voice_name == voice.name:
            engine.setProperty("voice", voice.id)
            break

    engine.say(text)
    engine.runAndWait()
