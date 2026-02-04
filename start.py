import os
import sys
import subprocess
import platform

VENV_DIR = "venv"
REQUIREMENTS = "requirements.txt"
APP_FILE = "app.py"

def is_venv_active():
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def create_venv():
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)

def get_python_executable():
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "python")

def install_dependencies():
    python_exe = get_python_executable()
    if not os.path.exists(python_exe):
        create_venv()

    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([python_exe, "-m", "pip", "install", "-r", REQUIREMENTS], check=True)
    
def start_app():
    python_exe = get_python_executable()
    subprocess.run([python_exe, APP_FILE])

def main():
    if not os.path.exists(VENV_DIR):
        create_venv()
        install_dependencies()
    else:
        python_exe = get_python_executable()
        result = subprocess.run(
            [python_exe, "-m", "pip", "list"],
            capture_output=True,
            text=True
        )
        if "dash" not in result.stdout:
            install_dependencies()

    start_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.exit(1)
