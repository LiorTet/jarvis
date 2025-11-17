import transcribe_from_mic

def listen() -> str:
    """
    Function to initialize the listening of main flow.
    """
    text = ""
    while not text.strip():
        print("Waiting for valid speech input...")
        text = transcribe_from_mic().strip()

    print("You said:", text)
    return text