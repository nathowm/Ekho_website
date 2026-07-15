import sqlite3
from datetime import date

con = sqlite3.connect('lieux_mirror.db')
cur = con.cursor()
today = date.today().isoformat()

def get_or_create(table, nom):
    cur.execute(f"INSERT OR IGNORE INTO {table} (nom) VALUES (?)", (nom,))
    cur.execute(f"SELECT id FROM {table} WHERE nom = ?", (nom,))
    return cur.fetchone()[0]

def add_services(lieu_id, noms):
    for n in noms:
        sid = get_or_create('services', n)
        cur.execute("INSERT OR IGNORE INTO lieu_services (lieu_id, service_id) VALUES (?,?)", (lieu_id, sid))

def add_tags(lieu_id, noms):
    for n in noms:
        tid = get_or_create('tags', n)
        cur.execute("INSERT OR IGNORE INTO lieu_tags (lieu_id, tag_id) VALUES (?,?)", (lieu_id, tid))

def append_source(lieu_id, note):
    cur.execute("SELECT source_donnees FROM lieux WHERE id = ?", (lieu_id,))
    (existing,) = cur.fetchone()
    existing = existing or ""
    new = existing + (f"\n[{today}] {note}" if existing else f"[{today}] {note}")
    cur.execute("UPDATE lieux SET source_donnees = ? WHERE id = ?", (new, lieu_id))

# --- id 51 : Pain Pan ---
add_tags(51, ["boulangerie de quartier bio, devanture jaune vif reconnaissable", "focaccia, pizza, croissants et cinnamon rolls faits maison chaque jour", "ambiance brute/atelier, jeune équipe visible aux fours", "file d'attente fréquente le matin"])
append_source(51, "Enrichissement WebSearch : note '3.9/5 sur 826 avis' trouvée mais source non clairement identifiée comme Google Maps (agrégateur générique) — jugée insuffisamment fiable, NON ajoutée en note_google conformément à la règle vérifié/agrégé.")

# --- id 52 : Le Molotov ---
cur.execute("UPDATE lieux SET note_google = ?, nombre_avis_google = ? WHERE id = ?", (4.6, 730, 52))
add_services(52, ["Salle de concert"])
add_tags(52, ["salle de concert intimiste au Cours Julien", "programmation musicale éclectique plusieurs soirs par semaine", "large choix de bières (bouteilles du monde + pression)", "ambiance conviviale, personnel apprécié"])
append_source(52, "Note Google 4.6 sur 730 avis explicitement attribuée à 'Google My Business' par la source WebSearch agrégée (sans fetch direct d'une fiche Google Maps synchronisée) — reportée en note_google mais flaguée AGRÉGÉE/non vérifiée par fetch direct.")

# --- id 53 : Mercato by Winesucker — VÉRIFIÉ via fetch direct restaurants-de-france.fr ---
cur.execute("UPDATE lieux SET note_google = ?, nombre_avis_google = ? WHERE id = ?", (4.6, 93, 53))
add_services(53, ["Toilettes", "Toilettes non genrées", "Wifi", "Bar disponible sur place", "Livraison", "Vente à emporter"])
add_tags(53, ["accessible en fauteuil roulant", "chiens acceptés (intérieur et extérieur)", "LGBTQ+ friendly", "safe place personnes trans", "plats bio et végétaliens", "cuisine d'inspiration arménienne par le chef-patron Fred, belle sélection de vins nature", "décor deux salles écharpes OM/Arsenal, comptoir orange", "avis clients très contrastés (plusieurs expériences de service décevantes à côté d'avis dithyrambiques) — reflété fidèlement"])
append_source(53, "VÉRIFIÉ via fetch direct restaurants-de-france.fr (fiche synchronisée Google Maps, MAJ 19/11/2025) : note 4.6/5 sur 93 avis. Bloc 'à propos' riche (LGBTQ+/trans safe place, bio/vegan). NB : avis très hétérogènes sur la qualité du service selon les visites — reflété fidèlement sans lisser.")

con.commit()
cur.execute("SELECT id, nom, note_google, nombre_avis_google FROM lieux WHERE id BETWEEN 51 AND 53 ORDER BY id")
for r in cur.fetchall(): print(r)
con.close()
print("OK batch 6 -- pass complete")
