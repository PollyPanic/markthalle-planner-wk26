"""
Startup-Script für sostool
Erstellt automatisch ein venv, installiert Dependencies und startet die App
"""
import os
import sys
import subprocess
import platform

# Pfade
VENV_DIR = "venv"
REQUIREMENTS = "requirements.txt"
APP_FILE = "app.py"

def is_venv_active():
    """Prüft, ob bereits ein venv aktiv ist"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def create_venv():
    """Erstellt ein neues virtual environment"""
    print("📦 Erstelle virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
    print("✅ Virtual environment erstellt!")

def get_python_executable():
    """Gibt den Pfad zum Python-Executable im venv zurück"""
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "python")

def install_dependencies():
    """Installiert die Dependencies aus requirements.txt"""
    python_exe = get_python_executable()
    if not os.path.exists(python_exe):
        create_venv()

    print("📦 Installiere Dependencies...")
    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([python_exe, "-m", "pip", "install", "-r", REQUIREMENTS], check=True)
    print("✅ Dependencies installiert!")

def start_app():
    """Startet die Dash-App"""
    python_exe = get_python_executable()
    print("🚀 Starte sostool App...")
    print("=" * 50)
    subprocess.run([python_exe, APP_FILE])

def main():
    """Hauptfunktion"""
    print("🎯 sostool - Markthalle Winterkongress 2026")
    print("=" * 50)

    # Prüfe ob venv existiert
    if not os.path.exists(VENV_DIR):
        print("ℹ️  Kein virtual environment gefunden")
        create_venv()
        install_dependencies()
    else:
        print("✅ Virtual environment gefunden")
        # Prüfe ob Dependencies installiert sind
        python_exe = get_python_executable()
        result = subprocess.run(
            [python_exe, "-m", "pip", "list"],
            capture_output=True,
            text=True
        )
        if "dash" not in result.stdout:
            print("ℹ️  Dependencies nicht installiert")
            install_dependencies()
        else:
            print("✅ Dependencies bereits installiert")

    # Starte die App
    start_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 App gestoppt")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        sys.exit(1)
