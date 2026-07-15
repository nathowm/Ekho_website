import sqlite3

con = sqlite3.connect('/tmp/lieux_db/lieux_mirror.db')
cur = con.cursor()
LID = 48


def get_or_create(table, nom):
    cur.execute(f"SELECT id FROM {table} WHERE nom = ?", (nom,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(f"INSERT INTO {table} (nom) VALUES (?)", (nom,))
    return cur.lastrowid


# --- site_web : site officiel trouvé (johnsilverbistroffee.fr), remplace le fallback Instagram ---
cur.execute("UPDATE lieux SET site_web=? WHERE id=?", ("https://www.johnsilverbistroffee.fr/", LID))

# --- horaires : correction via toutma.fr (08/01/2026, source la plus précise/détaillée, recoupée par
# WebSearch agrégé) -- lundi-vendredi 8h30-16h30, samedi 9h30-17h, fermé dimanche
# (remplace mardi-samedi 8h30-16h / fermé dim-lun retenu précédemment via love-spots) ---
cur.execute('DELETE FROM horaires_tranches WHERE lieu_id=?', (LID,))
horaires = {
    'Lundi': ('08:30', '16:30'), 'Mardi': ('08:30', '16:30'), 'Mercredi': ('08:30', '16:30'),
    'Jeudi': ('08:30', '16:30'), 'Vendredi': ('08:30', '16:30'), 'Samedi': ('09:30', '17:00'),
    'Dimanche': None,
}
for jour, tranche in horaires.items():
    if tranche is None:
        cur.execute('INSERT INTO horaires_tranches (lieu_id, jour, ferme) VALUES (?, ?, 1)', (LID, jour))
    else:
        cur.execute('INSERT INTO horaires_tranches (lieu_id, jour, ferme, heure_debut, heure_fin) VALUES (?, ?, 0, ?, ?)',
                     (LID, jour, tranche[0], tranche[1]))

# --- images : remplacées par 3 photos explicitement légendées (devanture, salle, recette)
# de l'article toutma.fr, bien plus fiables que des visuels non identifiés ---
cur.execute('DELETE FROM images WHERE lieu_id=?', (LID,))
new_images = [
    'https://toutma.fr/wp-content/uploads/2026/01/John-Silver_devanture_Cedric-Villetorte-©laurettecie-786x1024.jpeg',
    'https://toutma.fr/wp-content/uploads/2026/01/John-Silver_salle_3-©laurettecie-683x1024.jpeg',
    'https://toutma.fr/wp-content/uploads/2026/01/John-Silver_recette_2©laurettecie-scaled.jpeg',
]
for i, u in enumerate(new_images, start=1):
    cur.execute('INSERT INTO images (lieu_id, url, ordre) VALUES (?, ?, ?)', (LID, u, i))

# --- tags : nettoyage (Coffee Shop retiré, redondant avec le type "Café" ; Vegan/Végétarien
# déplacés vers services per Règle 14.7 ; capacité en couverts retirée car sources contradictoires
# (12 selon toutma vs 18-20 selon love-spots) ---
cur.execute('DELETE FROM lieu_tags WHERE lieu_id=?', (LID,))
for tag_nom in [
    "Vieux-Port",
    "Premier « bistroffee » 100% végétal de Marseille",
    "Micro-salle intimiste, mobilier bistrot (tables rondes pieds fonte)",
]:
    tid = get_or_create("tags", tag_nom)
    cur.execute("INSERT OR IGNORE INTO lieu_tags (lieu_id, tag_id) VALUES (?, ?)", (LID, tid))

# --- services : Vegan/Végétarien (reclassés depuis tags) ; PAS de vente à emporter (explicitement exclue) ---
cur.execute('DELETE FROM lieu_services WHERE lieu_id=?', (LID,))
for service_nom in ["Vegan", "Végétarien"]:
    sid = get_or_create("services", service_nom)
    cur.execute("INSERT OR IGNORE INTO lieu_services (lieu_id, service_id) VALUES (?, ?)", (LID, sid))

# --- phrases d'accroche (fermé le soir) ---
cur.execute('DELETE FROM phrases_accroche WHERE lieu_id=?', (LID,))
phrases = [
    (LID, 'Matin', "Toasts et lattes originaux (pandan latte) pour un petit-déjeuner 100% végétal, préparé sur place."),
    (LID, 'Midi', "Cuisine végane familière et copieuse : assiette complète, chili sin carne ou simili carbonara."),
    (LID, 'Après-midi', "Un goûter végétal au comptoir, entre pandan latte et dessert maison (crumble pomme-cannelle)."),
    (LID, 'Soir', None),
]
cur.executemany('INSERT INTO phrases_accroche (lieu_id, moment, phrase) VALUES (?, ?, ?)', phrases)

# --- source_donnees : recherche complémentaire ---
cur.execute('SELECT source_donnees FROM lieux WHERE id=?', (LID,))
src = cur.fetchone()[0] or ''
note = (
    "[2026-07-15] Recherche complémentaire (demande utilisateur 'complete John Silver') : "
    "le-grand-pastis.com (22/01/2026) et toutma.fr (08/01/2026) confirment le chef-gérant Cédric Villetorte "
    "(ex-brasserie Intercontinental Marseille, végan depuis 7 ans, formé à l'école Vert la Table). Cuisine "
    "100% végétale (ni oeufs, ni laitages, ni dérivés carnés) : toasts le matin, 6 plats salés le midi (carte "
    "courte, renouvelée tous les 2 mois), desserts maison (crumble pomme-cannelle). Spécialités citées : "
    "assiette complète (riz basmati semi-complet, quinoa, caponata, tofu brouillé, crème cajou), chili sin "
    "carne, simili carbonara, pinsa romana crème miso-tofu, winter cheeseburger végétal, cannellonis "
    "bolognaise/béchamel végétale, banane fondante/chantilly végétale. Boissons : lattes originaux (pandan "
    "latte). IMPORTANT : pas de vente à emporter, tout se déguste sur place (choix assumé de la maison) — "
    "aucun service 'vente à emporter' ajouté en conséquence. Horaires corrigés : lundi-vendredi 8h30-16h30, "
    "samedi 9h30-17h, fermé dimanche (source toutma.fr, plus précise et recoupée par WebSearch agrégé "
    "Wheree/JohnSilverBistroffee.fr — remplace mardi-samedi 8h30-16h/fermé dim-lun retenu via love-spots). "
    "Capacité en couverts contradictoire entre sources (12 selon toutma.fr, 18-20 selon love-spots) — "
    "retirée des tags pour éviter d'afficher un chiffre non fiable, remplacée par une description qualitative. "
    "Site officiel trouvé : johnsilverbistroffee.fr (remplace le fallback Instagram @johnsilver.ob en site_web). "
    "Note 9,6/10 trouvée mais sur une échelle non-Google (probablement TheFork/agrégateur) — NON reportée en "
    "note_google, conformément à la règle vérifié/agrégé. Aucune fiche Google Maps synchronisée trouvée sur "
    "restaurants-de-france.fr malgré recherche croisée — note_google laissée vide. 3 photos remplacées par des "
    "visuels explicitement légendés par toutma.fr (devanture avec le chef, salle, plat), plus fiables que la "
    "sélection précédente non identifiée."
)
new_src = src + ('\n' if src else '') + note
cur.execute("UPDATE lieux SET source_donnees=?, updated_at=datetime('now') WHERE id=?", (new_src, LID))

con.commit()

print('site_web:', cur.execute('SELECT site_web FROM lieux WHERE id=?', (LID,)).fetchone())
print('horaires:', cur.execute('SELECT jour, heure_debut, heure_fin FROM horaires_tranches WHERE lieu_id=? ORDER BY jour', (LID,)).fetchall())
print('images:', cur.execute('SELECT url FROM images WHERE lieu_id=? ORDER BY ordre', (LID,)).fetchall())
print('tags:', cur.execute("SELECT t.nom FROM lieu_tags lt JOIN tags t ON lt.tag_id=t.id WHERE lt.lieu_id=?", (LID,)).fetchall())
print('services:', cur.execute("SELECT s.nom FROM lieu_services ls JOIN services s ON ls.service_id=s.id WHERE ls.lieu_id=?", (LID,)).fetchall())
print('phrases:', cur.execute('SELECT moment, phrase FROM phrases_accroche WHERE lieu_id=?', (LID,)).fetchall())
con.close()
