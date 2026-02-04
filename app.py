"""
Haupteinstiegspunkt für die sostool Dash-Anwendung
"""
from src.content import app, server

if __name__ == '__main__':
    app.run(debug=True)
