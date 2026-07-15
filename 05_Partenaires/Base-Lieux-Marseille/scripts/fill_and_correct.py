import sqlite3
from pathlib import Path

DB_PATH = Path("lieux_mirror.db")
MOMENTS = ["Matin", "Midi", "Après-midi", "Soir"]
WINDOWS = {
    "Matin": (7*60, 11*60),
    "Midi": (11*60, 14*60+30),
    "Après-midi": (14*60+30, 18*60+30),
    "Soir": (18*60+30, 27*60),  # allow wrap to 3am next day represented as +24h
}

def to_minutes(hhmm):
    h, m = map(int, hhmm.split(":"))
    return h*60+m

def tranche_ranges(debut, fin):
    d = to_minutes(debut)
    f = to_minutes(fin)
    if f <= d:
        f += 24*60  # overnight
    return [(d, f)]

def overlaps(a_start, a_end, b_start, b_end):
    return a_start < b_end and b_start < a_end

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

# ---- Profiles for mechanical ambiance fill ----
def profile(moment, is_night_venue):
    if moment == "Matin":
        return dict(bruit="Faible", luminosite="Fort", musique="Faible", affluence="Faible", types=["Calme"])
    if moment == "Midi":
        return dict(bruit="Modéré", luminosite="Fort", musique="Faible", affluence="Fort", types=["Sociable"])
    if moment == "Après-midi":
        return dict(bruit="Modéré", luminosite="Fort", musique="Modéré", affluence="Modéré", types=["Sociable"])
    if moment == "Soir":
        if is_night_venue:
            return dict(bruit="Fort", luminosite="Faible", musique="Fort", affluence="Fort", types=["Dynamique"])
        else:
            return dict(bruit="Modéré", luminosite="Faible", musique="Modéré", affluence="Modéré", types=["Sociable"])

NIGHT_TYPES = {"Bar", "Bar dansant", "Bar à jeux", "Pub", "Café-concert"}

report = []

for lid in range(3, 32):
    row = cur.execute("SELECT nom FROM lieux WHERE id=?", (lid,)).fetchone()
    if not row:
        continue
    nom = row[0]
    types = [r[0] for r in cur.execute(
        "SELECT t.nom FROM types_lieu t JOIN lieu_types lt ON lt.type_id=t.id WHERE lt.lieu_id=?", (lid,))]
    is_night = any(t in NIGHT_TYPES for t in types)

    horaires = cur.execute("SELECT jour,ferme,heure_debut,heure_fin FROM horaires_tranches WHERE lieu_id=?", (lid,)).fetchall()
    # union of open windows (minutes) across the week
    open_ranges = []
    for jour, ferme, hd, hf in horaires:
        if ferme or not hd or not hf:
            continue
        open_ranges.extend(tranche_ranges(hd, hf))

    existing = {r[0]: r for r in cur.execute(
        "SELECT moment,bruit,luminosite,musique,affluence FROM ambiance_moment WHERE lieu_id=?", (lid,))}

    added = []
    for moment in MOMENTS:
        if moment in existing:
            continue
        w_start, w_end = WINDOWS[moment]
        is_open = any(overlaps(w_start, w_end, s, e) or overlaps(w_start+24*60, w_end+24*60, s, e) for s, e in open_ranges)
        if not is_open:
            cur.execute(
                "INSERT INTO ambiance_moment (lieu_id, moment, bruit, luminosite, musique, affluence) VALUES (?,?,?,?,?,?)",
                (lid, moment, "Non applicable", "Non applicable", "Non applicable", "Non applicable"))
            added.append((moment, "Non applicable (fermé)"))
        else:
            p = profile(moment, is_night)
            cur.execute(
                "INSERT INTO ambiance_moment (lieu_id, moment, bruit, luminosite, musique, affluence) VALUES (?,?,?,?,?,?)",
                (lid, moment, p["bruit"], p["luminosite"], p["musique"], p["affluence"]))
            for t in p["types"]:
                cur.execute(
                    "INSERT OR IGNORE INTO ambiance_types (lieu_id, moment, ambiance_type) VALUES (?,?,?)",
                    (lid, moment, t))
            added.append((moment, f"estimé ({p['bruit']}/{p['luminosite']}/{p['musique']}/{p['affluence']})"))
    report.append((lid, nom, added))

conn.commit()

for lid, nom, added in report:
    print(lid, nom)
    for m, v in added:
        print("   +", m, "->", v)

conn.close()
