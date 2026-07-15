import sqlite3

con = sqlite3.connect('/tmp/lieux_db/lieux_mirror.db')
cur = con.cursor()

# --- images : remplacées par 3 photos de l'article Toutma "Polpette, Farniente à Saint-Victor"
# (article centré sur la terrasse et la vue, donc bien plus pertinent que les plats du Grand Pastis) ---
cur.execute('DELETE FROM images WHERE lieu_id=22')
new_images = [
    'https://toutma.fr/wp-content/uploads/2026/05/polpette-marseille.jpg',
    'https://toutma.fr/wp-content/uploads/2026/05/polpette-marseille-restaurant-768x1024.jpg',
    'https://toutma.fr/wp-content/uploads/2026/05/polpette-restaurant-576x1024.jpg',
]
for i, u in enumerate(new_images, start=1):
    cur.execute('INSERT INTO images (lieu_id, url, ordre) VALUES (?, ?, ?)', (22, u, i))

# --- cadre : Intérieur -> Mixte (salle + au moins une terrasse avec vue confirmées) ---
cur.execute("UPDATE lieux SET cadre='Mixte' WHERE id=22")

# --- site_web : pas de site officiel trouvé, mais lien Instagram confirmé (cité par le-grand-pastis.com) ---
cur.execute("UPDATE lieux SET site_web=? WHERE id=22", ("https://www.instagram.com/polpettetrattoria/",))

# --- source_donnees : recherche complémentaire ---
cur.execute('SELECT source_donnees FROM lieux WHERE id=22')
src = cur.fetchone()[0] or ''
note = (
    "[2026-07-15] Recherche complémentaire (toutma.fr, 04/05/2026, 'Polpette, Farniente à Saint-Victor') : "
    "Polpette a repris l'ancienne terrasse du restaurant La Savonnerie (mêmes propriétaires). Deux espaces "
    "extérieurs confirmés : une terrasse juste devant l'entrée (sous le four à navettes), en travaux de "
    "réaménagement au 04/05/2026 pour un cadre plus intime ; et une AUTRE terrasse avec vue sur la rade "
    "marseillaise, déjà en service (mentionnée explicitement : 'on profite de l'autre terrasse avec vue sur la "
    "rade marseillaise, un Spritz à la main'). Champ cadre mis à jour Intérieur -> Mixte en conséquence. Photos "
    "remplacées par 3 visuels de cet article (image de une + 2 photos verticales), plus pertinents pour "
    "montrer le lieu/la terrasse/la vue que les gros plans de plats du Grand Pastis utilisés précédemment. "
    "Site web officiel : aucun trouvé malgré recherche croisée (Google, PagesJaunes, WebSearch ciblé) — "
    "Instagram @polpettetrattoria (lien confirmé via le-grand-pastis.com) utilisé comme site_web par défaut, "
    "conforme à la convention du projet pour les lieux sans site propre. Note Google : toujours aucune fiche "
    "Google Maps synchronisée trouvée sur restaurants-de-france.fr ni ailleurs (établissement ouvert début "
    "mars 2026, probablement pas encore assez d'avis/pas encore repris par les annuaires synchronisés) — champ "
    "laissé vide plutôt que d'agréger une note non fiable. Horaires précis : toujours non trouvés malgré "
    "recherche élargie (WebSearch ciblé, PagesJaunes, Instagram) ; confirmé en revanche un service midi (pinsa/"
    "polpette) ET un service soir (carte tapas) tous les jours a priori — horaires exacts non publiés, à "
    "confirmer par téléphone (04 91 81 53 68)."
)
new_src = src + ('\n' if src else '') + note
cur.execute("UPDATE lieux SET source_donnees=?, updated_at=datetime('now') WHERE id=22", (new_src,))

# --- services : actuellement vide -> ajouter Terrasse (justifié par la recherche ci-dessus) ---
def get_or_create(table, nom):
    cur.execute(f"SELECT id FROM {table} WHERE nom = ?", (nom,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(f"INSERT INTO {table} (nom) VALUES (?)", (nom,))
    return cur.lastrowid

for service_nom in ["Terrasse", "Réservations acceptées"]:
    sid = get_or_create("services", service_nom)
    cur.execute("INSERT OR IGNORE INTO lieu_services (lieu_id, service_id) VALUES (?, ?)", (22, sid))

con.commit()

cur.execute('SELECT url FROM images WHERE lieu_id=22 ORDER BY ordre')
print('images:', cur.fetchall())
cur.execute('SELECT cadre, site_web FROM lieux WHERE id=22')
print('cadre/site_web:', cur.fetchone())
cur.execute("SELECT s.nom FROM lieu_services ls JOIN services s ON ls.service_id=s.id WHERE ls.lieu_id=22")
print('services:', cur.fetchall())
con.close()
