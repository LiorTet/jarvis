import subprocess
import jarvis.config.settings as cfg


OLLAMA_PATH = cfg.OLLAMA_PATH


def is_model_installed(model="phi3:mini") -> bool:
    """
    Check if model is installed at the beggining of the run
    Args
        model (str): specific model to check
    """
    try:
        # List installed models using `ollama list`
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )
        # Check if model name appears in the list output
        return model in result.stdout
    except subprocess.CalledProcessError as e:
        print("Error checking installed models:", e)
        return False


def install_model_if_needed(model="phi3:mini"):
    """
    Install model.
    Args
        model (str): model to install.
    """
    if is_model_installed(model):
        print(f"Model '{model}' is already installed.")
    else:
        print(f"Model '{model}' not found. Installing now...")
        try:
            subprocess.run(["ollama", "pull", model], check=True)
            print(f"Model '{model}' installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install model '{model}':", e)
