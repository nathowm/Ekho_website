import sqlite3

con = sqlite3.connect('/tmp/lieux_db/lieux_mirror.db')
cur = con.cursor()

cur.execute('DELETE FROM images WHERE lieu_id=53')
new_images = [
    'https://lh3.googleusercontent.com/gps-cs-s/AG0ilSzpkArPba_FknncUdsRR-AvoL6ixUuxPEP9zZ_3W7oa_dRxPbfLzE1mOP2A0lrKkY1NQa03DagAu0an7JgwQmwHN5Sq690tdojGSriIPywfZXbsxUo7OgfHeMcFXPilPXz7V5bB=w1600-h1200-k-no',
    'https://lh3.googleusercontent.com/gps-cs-s/AG0ilSxCIecIaJGAstbs0ke5d1ooNLQyi2sUUEK5SF4PJeaGcpxsQo1epZNjBaw5YgYp3VyBZITRqXkcshyHdwRK-Cgtc-F1vIuycPE7ztqbtNd9zvJOak8KY3gdz44KQ_0DNm-Dm1o=w1600-h1200-k-no',
    'https://lh3.googleusercontent.com/gps-cs-s/AG0ilSxgDPAuzZxIRrNhxBiiKiIdS8Y9x5WB635aoIQYAD_jGdozxNTZewvNRImHTMK1YSOD3uI5MymKk3yBKib7N-Pufv-8I9jHz5nWjILDLoouaI9PvySzMTJwK3XI-HPRTe2lD5WC_A=w1600-h1200-k-no',
]
for i, u in enumerate(new_images, start=1):
    cur.execute('INSERT INTO images (lieu_id, url, ordre) VALUES (?, ?, ?)', (53, u, i))

cur.execute('SELECT source_donnees FROM lieux WHERE id=53')
src = cur.fetchone()[0] or ''
note = (
    "[2026-07-15] Photos remplacées par 3 images HD tirées de la galerie complète (33 photos) de la fiche "
    "restaurant.restaurants-de-france.fr (fiche Google Maps synchronisée, MAJ 19/11/2025) — au lieu des 3 "
    "vignettes génériques (format 'places/...s1600-w640') utilisées précédemment, moins qualitatives."
)
new_src = src + ('\n' if src else '') + note
cur.execute("UPDATE lieux SET source_donnees=?, updated_at=datetime('now') WHERE id=53", (new_src,))
con.commit()

cur.execute('SELECT url FROM images WHERE lieu_id=53 ORDER BY ordre')
for r in cur.fetchall():
    print(r[0])
con.close()
