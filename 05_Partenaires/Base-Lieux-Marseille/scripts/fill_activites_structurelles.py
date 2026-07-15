import sqlite3
from pathlib import Path

DB_PATH = Path("lieux_mirror.db")
MOMENTS = ["Matin", "Midi", "Après-midi", "Soir"]
WINDOWS = {
    "Matin": (7*60, 11*60),
    "Midi": (11*60, 14*60+30),
    "Après-midi": (14*60+30, 18*60+30),
    "Soir": (18*60+30, 27*60),
}
STRUCT = ["Lire","Travailler","Jeux de société","Jeux vidéos","Écouter de la musique",
          "Manger","Boire un verre","Boire un café","Goûter"]

BAR_TYPES = {"Bar", "Bar dansant", "Pub", "Café-concert"}
GAME_BAR = {"Bar à jeux"}
CAFE_TYPES = {"Café", "Bistrot", "Librairie-café", "Cybercafé"}
COWORK_TYPES = {"Coworking", "Cybercafé"}
RESTO_TYPES = {"Restaurant", "Bistrot"}

def to_minutes(hhmm):
    h, m = map(int, hhmm.split(":"))
    return h*60+m

def tranche_ranges(debut, fin):
    d = to_minutes(debut); f = to_minutes(fin)
    if f <= d: f += 24*60
    return [(d, f)]

def overlaps(a_s, a_e, b_s, b_e):
    return a_s < b_e and b_s < a_e

def decide(activite, moment, types, is_open):
    if not is_open:
        return "-"
    is_bar = bool(types & BAR_TYPES)
    is_gamebar = bool(types & GAME_BAR)
    is_cafe = bool(types & CAFE_TYPES)
    is_cowork = bool(types & COWORK_TYPES)
    is_resto = bool(types & RESTO_TYPES)

    if activite == "Lire":
        return "S" if (is_cafe or is_cowork) and moment != "Soir" else "-"
    if activite == "Travailler":
        return "S" if (is_cafe or is_cowork) and moment != "Soir" else "-"
    if activite == "Jeux de société":
        return "S" if is_gamebar and moment in ("Midi", "Après-midi", "Soir") else "-"
    if activite == "Jeux vidéos":
        return "-"
    if activite == "Écouter de la musique":
        return "S" if is_bar and moment in ("Après-midi", "Soir") else "-"
    if activite == "Manger":
        return "S" if is_resto and moment in ("Midi", "Soir") else "-"
    if activite == "Boire un verre":
        return "S" if (is_bar or is_resto) and moment in ("Après-midi", "Soir") else "-"
    if activite == "Boire un café":
        return "S" if is_cafe and moment != "Soir" else "-"
    if activite == "Goûter":
        return "S" if is_cafe and moment == "Après-midi" else "-"
    return "-"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()
cur2 = conn.cursor()
cur3 = conn.cursor()

act_ids = {nom: aid for aid, nom in cur.execute("SELECT id, nom FROM activites").fetchall()}

report = []
for lid, nom in cur.execute("SELECT id, nom FROM lieux ORDER BY id").fetchall():
    types = set(r[0] for r in cur2.execute(
        "SELECT t.nom FROM lieu_types lt JOIN types_lieu t ON t.id=lt.type_id WHERE lt.lieu_id=?", (lid,)).fetchall())

    horaires = cur2.execute(
        "SELECT jour,ferme,heure_debut,heure_fin FROM horaires_tranches WHERE lieu_id=?", (lid,)).fetchall()
    open_ranges = []
    for jour, ferme, hd, hf in horaires:
        if ferme or not hd or not hf:
            continue
        open_ranges.extend(tranche_ranges(hd, hf))

    def is_open(moment):
        w_s, w_e = WINDOWS[moment]
        return any(overlaps(w_s, w_e, s, e) or overlaps(w_s+24*60, w_e+24*60, s, e) for s, e in open_ranges)

    present = set(r[0] for r in cur3.execute("""
        SELECT DISTINCT a.nom FROM activites_priorite ap JOIN activites a ON a.id=ap.activite_id
        WHERE ap.lieu_id=?""", (lid,)).fetchall())

    added = []
    for act in STRUCT:
        if act in present:
            continue
        aid = act_ids[act]
        for m in MOMENTS:
            val = decide(act, m, types, is_open(m))
            cur.execute(
                "INSERT INTO activites_priorite (lieu_id, activite_id, moment, valeur) VALUES (?,?,?,?)",
                (lid, aid, m, val))
            added.append((act, m, val))
    if added:
        report.append((lid, nom, added))

conn.commit()
for lid, nom, added in report:
    print(lid, nom, "-> ajout de", len(added)//4, "activité(s) structurelle(s)")
conn.close()
print("Total lieux traités:", len(report))
