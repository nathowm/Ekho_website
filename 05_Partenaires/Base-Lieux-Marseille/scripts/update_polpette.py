import sqlite3

con = sqlite3.connect('/tmp/lieux_db/lieux_mirror.db')
cur = con.cursor()

# --- images : remplacer par une sélection plus représentative (façade + 2 plats signature) ---
cur.execute('DELETE FROM images WHERE lieu_id=22')
new_images = [
    'https://www.le-grand-pastis.com/wp-content/uploads/2026/04/Polpette-huit.png',
    'https://www.le-grand-pastis.com/wp-content/uploads/2026/04/Polpette-quatre-768x1024.png',
    'https://www.le-grand-pastis.com/wp-content/uploads/2026/04/Polpette-six-fotor-20260402151236.png',
]
for i, u in enumerate(new_images, start=1):
    cur.execute('INSERT INTO images (lieu_id, url, ordre) VALUES (?, ?, ?)', (22, u, i))

# --- contenu enrichi : source_donnees ---
cur.execute('SELECT source_donnees FROM lieux WHERE id=22')
src = cur.fetchone()[0] or ''
note = (
    "[2026-07-15] Enrichissement contenu + photos via relecture complète de l'article le-grand-pastis.com "
    "(02/04/2026) : cheffe Stella (originaire de la Belle-de-Mai, racines corses et marseillaises), ancienne "
    "de la boutique Aussih (4-Septembre, 6 ans) où elle avait réorienté la carte vers une cuisine méditerranéenne "
    "réconfortante ; ouverture Polpette début mars 2026 au pied de l'abbaye Saint-Victor, face au Vieux-Port. "
    "Carte détaillée : pinsa romaine (pâte blé/soja/riz, versions parma/margherita/anchois), polpette de boeuf "
    "en sauce tomate, polpette ricotta (à partager), vitello tonnato, arancini, linguine polpette, artichauts "
    "rôtis sur ricotta fouettée à l'huile pimentée, poivrons grillés-câprons/moutarde/pistou basilic, focaccia "
    "maison ; desserts tiramisu, panna cotta, gâteau chocolat sans farine (chantilly pistache maison). Midi : "
    "pinsa/plats ; soir : bascule sur une carte tapas. Équipe en salle : Felipe, Nico, Romane, Gianni, Geoffrey. "
    "Photos remplacées par une sélection plus représentative (façade/enseigne + 2 plats signature en gros plan, "
    "au lieu de 2 visuels non identifiés précédemment) — mêmes 8 photos disponibles dans la galerie de "
    "l'article, choix affiné pour mieux refléter le lieu et la cuisine."
)
new_src = src + ('\n' if src else '') + note
cur.execute("UPDATE lieux SET source_donnees=?, updated_at=datetime('now') WHERE id=22", (new_src,))

# --- tag signature affiné ---
cur.execute("SELECT tag_id FROM lieu_tags lt JOIN tags t ON lt.tag_id=t.id WHERE lt.lieu_id=22 AND t.nom='pinsa et polpettes de bœuf signature'")
row = cur.fetchone()
if row:
    cur.execute("UPDATE tags SET nom=? WHERE id=?", ("Pinsa romaine et polpette de bœuf en sauce tomate, gâteau chocolat sans farine", row[0]))

con.commit()
cur.execute('SELECT url FROM images WHERE lieu_id=22 ORDER BY ordre')
print('images:', cur.fetchall())
cur.execute("SELECT t.nom FROM lieu_tags lt JOIN tags t ON lt.tag_id=t.id WHERE lt.lieu_id=22")
print('tags:', cur.fetchall())
con.close()
