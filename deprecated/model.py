import subprocess


def ask_ollama(prompt: str, model="phi3:mini"):
    """
    Prompt the model.
    Args
        prompt (str): text to model.
        model (str): model to use.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error running Ollama:", e.stderr)
        return None
