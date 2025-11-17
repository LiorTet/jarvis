def exit_cond() -> bool:
    """
    Function to initialize the listening of main flow.
    """
    cleaned_text = text.lower().strip()
    if any(re.search(rf"\b{kw}\b", cleaned_text) for kw in EXIT_COMMANDS):
        print("Exiting Jarvis. Goodbye!")
        speak("Goodbye!")
        return True
    else:
        return False