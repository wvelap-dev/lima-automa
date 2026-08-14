"""
Lima Automa - Configuración del Proyecto
==========================================
Automatización de adquisición de clientes para restaurantes en Lima, Perú
"""

# === CONFIGURACIÓN GENERAL ===
PROJECT_NAME = "Lima Automa"
VERSION = "0.2.0"

# === DOMINIO ===
DOMAIN = "lima-aa91.vercel.app"
BASE_URL = f"https://{DOMAIN}"

# === ZONA OBJETIVO ===
DEFAULT_LOCATION = "Lima, Perú"
DISTRICTS = [
    "Miraflores",
    "San Isidro",
    "Barranco",
    "Surco",
    "La Molina",
    "Jesús María",
    "Lince",
    "Pueblo Libre",
    "San Borja",
    "Magdalena del Mar",
]

# === SECTOR OBJETIVO ===
TARGET_SECTOR = "Restaurantes"
SEARCH_QUERIES = [
    "restaurante",
    "restaurant",
    "comida rapida",
    "cafeteria",
    "comida peruana",
    "parrilla",
    "cevicheria",
    "chifa",
]

# === SCORING DE PRIORIDAD ===
# Un restaurante con estos indicadores tiene más probabilidad de necesitar ayuda
SCORING_RULES = {
    "low_reviews": {"max_reviews": 20, "score": +30},       # Pocas reseñas = necesita ayuda
    "low_rating": {"max_stars": 4.0, "score": +20},         # Mala calificación
    "no_website": {"penalty": -5, "score": +15},             # Sin página web
    "no_instagram": {"penalty": -3, "score": +10},           # Sin Instagram activo
    "competitor_nearby": {"count": 3, "score": +25},         # Muchos competidores cerca
}

# === MENSAJES ===
MESSAGES_DIR = "templates/messages"
OUTPUT_DIR = "data"
