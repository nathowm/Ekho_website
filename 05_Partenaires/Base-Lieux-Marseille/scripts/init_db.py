"""
Initialise la base miroir locale (SQLite) : crée le schéma et pré-remplit
les tables de référence (types de lieu, activités, services, tags)
d'après le formulaire fourni.

Usage :
    python3 init_db.py
"""
import sqlite3
from pathlib import Path

DB_PATH = Path('/tmp/lieux_db/lieux_mirror.db')
SCHEMA_PATH = Path('/tmp/lieux_db/schema.sql')

TYPES_LIEU = [
    "Bar", "Bar dansant", "Bar à jeux", "Bistrot", "Café", "Café-concert",
    "Coworking", "Cybercafé", "Librairie", "Librairie-café", "Pub", "Restaurant",
]

# (nom, type) — type = 'priorite' (P/S/-) ou 'frequence' (F/O/R/-)
ACTIVITES = [
    ("Lire", "priorite"),
    ("Travailler", "priorite"),
    ("Jeux de société", "priorite"),
    ("Jeux vidéos", "priorite"),
    ("Écouter de la musique", "priorite"),
    ("Manger", "priorite"),
    ("Boire un verre", "priorite"),
    ("Boire un café", "priorite"),
    ("Goûter", "priorite"),
    ("Divertissement", "frequence"),
]

SERVICES = [
    "Wifi", "Prise électrique", "Assis", "Quotidiens / Journaux", "Livres",
    "Parking", "Accès handicap", "Terrasse", "Climatisation", "Dés",
    "Animaux acceptés", "Micro", "Télévision", "Billard", "Fléchettes",
    "Piano", "Guitare", "Terrasse chauffée",
]

# Tags observés sur la fiche exemple fournie — liste de départ, à enrichir au fil de l'eau
TAGS = [
    "Bière Artisanale", "Café Spécialisé", "Cosy", "Café Artisanal",
    "Cocktails", "Cuisine Bistronomie", "Jeux Vidéos", "Jeux de société",
    "Lieu Culturel", "Patisserie Japonaise",
]


def init_db():
    fresh = not DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())

    cur = conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO types_lieu (nom) VALUES (?)", [(t,) for t in TYPES_LIEU])
    cur.executemany("INSERT OR IGNORE INTO activites (nom, type) VALUES (?, ?)", ACTIVITES)
    cur.executemany("INSERT OR IGNORE INTO services (nom) VALUES (?)", [(s,) for s in SERVICES])
    cur.executemany("INSERT OR IGNORE INTO tags (nom) VALUES (?)", [(t,) for t in TAGS])
    conn.commit()
    conn.close()
    print(f"{'Base créée' if fresh else 'Base mise à jour'} : {DB_PATH}")


if __name__ == "__main__":
    init_db()
