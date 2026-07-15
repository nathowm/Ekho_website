import sqlite3
from pathlib import Path
from collections import defaultdict

DB_PATH = Path("lieux_mirror.db")
MOMENTS = ["Matin", "Midi", "Après-midi", "Soir"]
WINDOWS = {
    "Matin": (7*60, 11*60),
    "Midi": (11*60, 14*60+30),
    "Après-midi": (14*60+30, 18*60+30),
    "Soir": (18*60+30, 27*60),
}

def to_minutes(hhmm):
    h, m = map(int, hhmm.split(":"))
    return h*60+m

def tranche_ranges(debut, fin):
    d = to_minutes(debut); f = to_minutes(fin)
    if f <= d: f += 24*60
    return [(d, f)]

def overlaps(a_s, a_e, b_s, b_e):
    return a_s < b_e and b_s < a_e

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()
cur2 = conn.cursor()

report = []

for lid, nom in cur.execute("SELECT id, nom FROM lieux ORDER BY id").fetchall():
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

    rows = cur2.execute("""
        SELECT ap.activite_id, a.nom, ap.moment, ap.valeur
        FROM activites_priorite ap JOIN activites a ON a.id = ap.activite_id
        WHERE ap.lieu_id=?""", (lid,)).fetchall()
    if not rows:
        continue

    per_act = defaultdict(dict)   # activite_id -> {moment: valeur}
    act_names = {}
    act_type = {}
    for aid, anom, moment, valeur in rows:
        per_act[aid][moment] = valeur
        act_names[aid] = anom

    added = []
    for aid, moments_vals in per_act.items():
        missing = [m for m in MOMENTS if m not in moments_vals]
        if not missing:
            continue
        # determine type (priorite vs frequence) from existing values
        existing_vals = set(moments_vals.values())
        is_freq = existing_vals & {"F", "O", "R"}
        for m in missing:
            if not is_open(m):
                val = "-"
            else:
                # nearest neighbor by moment order (circular distance over MOMENTS)
                idx_m = MOMENTS.index(m)
                best = None
                best_dist = 99
                for other_m, other_v in moments_vals.items():
                    if other_v == "-":
                        continue
                    idx_o = MOMENTS.index(other_m)
                    dist = min(abs(idx_m-idx_o), 4-abs(idx_m-idx_o))
                    if dist < best_dist:
                        best_dist = dist
                        best = other_v
                if best is None:
                    val = "S"  # valeur par défaut prudente
                else:
                    # légèrement dégradé par rapport à la valeur de référence
                    if is_freq:
                        val = best  # garder cohérent pour Divertissement
                    else:
                        val = "S" if best == "P" else best
            cur.execute(
                "INSERT INTO activites_priorite (lieu_id, activite_id, moment, valeur) VALUES (?,?,?,?)",
                (lid, aid, m, val))
            added.append((act_names[aid], m, val))

    if added:
        report.append((lid, nom, added))

conn.commit()
for lid, nom, added in report:
    print(lid, nom)
    for act, m, v in added:
        print("   +", act, m, "->", v)
conn.close()
