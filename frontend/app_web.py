"""
app_web.py — Server Flask principale per la Trading AI App Web UI.

Questo file è il punto di ingresso dell'applicazione web. Si occupa di:
1. Configurare il server Flask
2. Registrare le API per il backtesting e i dati
3. Servire le pagine HTML del frontend
4. Aggiungere il percorso principale del progetto al sys.path
   per poter importare i moduli esistenti (Calibrazione, data_fetcher, agenti)
"""

import sys
import os

# Aggiungiamo la cartella ROOT del progetto al percorso di Py
# così Flask trova Calibrazione.py, data_fetcher.py, agents/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from flask import Flask, render_template
from flask_cors import CORS
import Calibrazione

# Importiamo i Blueprint delle API (vedi frontend/api/)
from api.backtesting import backtesting_bp
from api.data import data_bp

# Creiamo l'app Flask, indicando dove trovare i template HTML e i file statici
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# CORS: permette al JavaScript del browser di fare chiamate API allo stesso server
CORS(app)

# ------------------------------------------------------------------
# REGISTRAZIONE DELLE API
# ------------------------------------------------------------------
app.register_blueprint(backtesting_bp, url_prefix="/api/backtest")
app.register_blueprint(data_bp, url_prefix="/api/data")

# ------------------------------------------------------------------
# ROTTE PRINCIPALI (Pagine HTML)
# ------------------------------------------------------------------

@app.route("/")
def index():
    """Redirect alla pagina di backtesting (sezione principale)"""
    return render_template("backtesting.html", config_calibrazione=Calibrazione)

@app.route("/backtesting")
def backtesting():
    """Pagina principale del Backtesting"""
    return render_template("backtesting.html", config_calibrazione=Calibrazione)

# ------------------------------------------------------------------
# AVVIO SERVER
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("  🚀 TRADING AI APP — WEB UI IN AVVIO")
    print("  📊 Apri il browser su: http://localhost:5001")
    print("=" * 60)
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True,
        use_reloader=False  # Disabilitato per evitare doppio caricamento degli agenti
    )
