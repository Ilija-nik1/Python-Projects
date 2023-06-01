import subprocess
import sys

def update_pip():
    """
    Update pip to the latest version using subprocess module.
    """
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print("Pip has been successfully updated to the latest version.")
    except subprocess.CalledProcessError as error:
        print(f"Error while updating pip: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"An error occurred while updating pip: {error}")
        sys.exit(1)

if __name__ == "__main__":
    update_pip()