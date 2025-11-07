import os
import firebase_admin
from firebase_admin import credentials, firestore
import json

# --- Inicialización Firebase ---
# Intentar obtener las credenciales desde la variable de entorno
firebase_config_str = os.environ.get("FIREBASE_CONFIG")

if firebase_config_str:
    firebase_config = json.loads(firebase_config_str)
    cred = credentials.Certificate(firebase_config)
else:
    # Si estás corriendo localmente, usa el archivo .json
    cred = credentials.Certificate("firebase_config.json")

firebase_admin.initialize_app(cred)
db = firestore.client()
