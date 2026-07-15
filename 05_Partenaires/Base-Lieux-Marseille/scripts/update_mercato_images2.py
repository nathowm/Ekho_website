import sqlite3

con = sqlite3.connect('/tmp/lieux_db/lieux_mirror.db')
cur = con.cursor()

cur.execute('DELETE FROM images WHERE lieu_id=53')
new_images = [
    # photo "cover" par défaut choisie par Google/Mapstr pour ce lieu (généralement représentative
    # du lieu lui-même, façade/salle, plutôt qu'un plat candid) — remise en position 1
    'https://lh3.googleusercontent.com/places/ANJU3DuWEXHuqUrsbKk5i9ZROfxXjdMT3c2Rxrm6DGaf_HTzDTDjQp72ALG7nb4dT_WmXWKM-AUhM3ANcCHiV3X9jyuaaIk7XfvJVYw=s1600-w640',
    'https://lh3.googleusercontent.com/gps-cs-s/AG0ilSzpkArPba_FknncUdsRR-AvoL6ixUuxPEP9zZ_3W7oa_dRxPbfLzE1mOP2A0lrKkY1NQa03DagAu0an7JgwQmwHN5Sq690tdojGSriIPywfZXbsxUo7OgfHeMcFXPilPXz7V5bB=w1600-h1200-k-no',
    'https://lh3.googleusercontent.com/gps-cs-s/AG0ilSxCIecIaJGAstbs0ke5d1ooNLQyi2sUUEK5SF4PJeaGcpxsQo1epZNjBaw5YgYp3VyBZITRqXkcshyHdwRK-Cgtc-F1vIuycPE7ztqbtNd9zvJOak8KY3gdz44KQ_0DNm-Dm1o=w1600-h1200-k-no',
]
for i, u in enumerate(new_images, start=1):
    cur.execute('INSERT INTO images (lieu_id, url, ordre) VALUES (?, ?, ?)', (53, u, i))

cur.execute('SELECT source_donnees FROM lieux WHERE id=53')
src = cur.fetchone()[0] or ''
note = (
    "[2026-07-15] Retour utilisateur : les 3 photos HD ajoutées le 15/07/2026 ne montraient que des plats, "
    "aucune ne montrait le lieu. Limite technique : aucun outil de cette session ne permet un aperçu visuel "
    "des photos (navigateur bloqué sur restaurants-de-france.fr/Google Maps, téléchargement direct des URLs "
    "Google bloqué par le pare-feu du bac à sable) — sélection faite à l'aveugle sur la seule position dans la "
    "galerie. Correctif : réintégration en position 1 de la photo 'cover' par défaut choisie par Google/Mapstr "
    "pour ce lieu (généralement représentative de la façade/salle plutôt qu'un plat candid), 2 photos HD "
    "conservées en position 2-3. Site officiel marseille-tourisme.com consulté en complément : confirme 06 20 "
    "25 25 66 comme téléphone public (absent jusqu'ici), horaires officiels 18h-23h30 lundi-samedi (fermé "
    "dimanche, légèrement plus tard que les 18h-23h précédemment retenus), capacité 40 couverts / 2 salles, "
    "décor 'écharpes OM et Arsenal, murs bruts, comptoir orange (tangerine)' — cohérent avec les tags/services "
    "existants. Chef en cuisine : Justine Pruvot (le patron Fred Semerdjian, également derrière Winesucker, "
    "supervise l'ensemble)."
)
new_src = src + ('\n' if src else '') + note
cur.execute("UPDATE lieux SET source_donnees=?, updated_at=datetime('now') WHERE id=53", (new_src,))

# téléphone public
cur.execute("UPDATE lieux SET telephone_public=? WHERE id=53", ("06 20 25 25 66",))

# horaires officiels marseille-tourisme.com : lundi-samedi 18h-23h30 (fermé dimanche),
# vs 18h-23h lundi-vendredi (fermé sam-dim) précédemment retenu via Mapstr
cur.execute('DELETE FROM horaires_tranches WHERE lieu_id=53')
horaires = {
    'Lundi': ('18:00', '23:30'), 'Mardi': ('18:00', '23:30'), 'Mercredi': ('18:00', '23:30'),
    'Jeudi': ('18:00', '23:30'), 'Vendredi': ('18:00', '23:30'), 'Samedi': ('18:00', '23:30'),
    'Dimanche': None,
}
for jour, tranche in horaires.items():
    if tranche is None:
        cur.execute('INSERT INTO horaires_tranches (lieu_id, jour, ferme) VALUES (?, ?, 1)', (53, jour))
    else:
        cur.execute('INSERT INTO horaires_tranches (lieu_id, jour, ferme, heure_debut, heure_fin) VALUES (?, ?, 0, ?, ?)',
                     (53, jour, tranche[0], tranche[1]))

# phrase d'accroche : corriger l'attribution du chef (Justine Pruvot cuisine, Fred Semerdjian est le patron)
cur.execute("SELECT phrase FROM phrases_accroche WHERE lieu_id=53 AND moment='Soir'")
row = cur.fetchone()
if row:
    cur.execute(
        "UPDATE phrases_accroche SET phrase=? WHERE lieu_id=53 AND moment='Soir'",
        ("Cave à manger conviviale : vins nature et tapas végétales sous les couleurs foot OM/Arsenal, au comptoir orange.",),
    )

# samedi désormais ouvert : mettre à jour l'ambiance/activités du samedi n'est pas nécessaire
# (le schéma raisonne par moment de la journée, pas par jour) — pas de changement requis ici.

con.commit()
cur.execute('SELECT url FROM images WHERE lieu_id=53 ORDER BY ordre')
for r in cur.fetchall():
    print(r[0])
cur.execute('SELECT telephone_public FROM lieux WHERE id=53')
print('tel:', cur.fetchone())
con.close()
