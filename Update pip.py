import subprocess

def update_pip():
    subprocess.call(["python", "-m", "pip", "install", "--upgrade", "pip"])

if __name__ == "__main__":
    update_pip()