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

# --- id 1 : AKU ---
add_tags(1, ["décoration japonaise raffinée", "ambiance minimaliste et élégante", "cheesecakes japonais légers", "fruit sando", "taiyaki"])
append_source(1, "Enrichissement WebSearch (à propos/avis) : pâtisserie japonaise, ambiance zen/épurée façon ville japonaise contemporaine. Aucune note Google fiable trouvée (pas de fiche restaurants-de-france.fr ni note Google chiffrée) — non ajoutée pour éviter fabrication.")

# --- id 2 : KRM ---
add_services(2, ["Galerie photo", "Boutique"])
add_tags(2, ["café-galerie hybride et solidaire", "ambiance chaleureuse et détendue", "expositions photo locales", "spécialités maghrébines (eau de rose, tahini latte)", "10% des ventes reversés à des associations"])
append_source(2, "Enrichissement WebSearch (à propos/avis) : lieu hybride café/galerie/boutique près de Noailles, ambiance conviviale. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 3 : Bistrot Georges (rating déjà présent : 4.4/940, ajout services/tags) ---
add_services(3, ["Terrasse", "Service à table"])
add_tags(3, ["salade caesar emblématique", "options végétariennes copieuses", "desserts maison", "ambiance conviviale quartier Camas", "terrasse animée"])
append_source(3, "Enrichissement WebSearch complémentaire (à propos/avis) : confirme terrasse vivante, cuisine fraîche/saine, salade caesar signature, ambiance conviviale ~10 ans d'existence sur le boulevard Chave.")

# --- id 4 : Black Unicorn ---
cur.execute("UPDATE lieux SET note_google = ? WHERE id = ?", (4.2, 4))
add_tags(4, ["pub à thème anglais", "soirées à thème (poker lundi, DJ vendredi, foot/rugby)", "ambiance conviviale quartier", "peut être exigu aux heures d'affluence"])
append_source(4, "Note Google 4.2 trouvée via WebSearch agrégé (non confirmée par fetch direct d'une fiche synchronisée Google Maps type restaurants-de-france.fr) — à considérer comme AGRÉGÉE/non vérifiée. Nombre d'avis non trouvé.")

# --- id 5 : La Rêveuse ---
add_tags(5, ["librairie-café", "ambiance lumineuse et conviviale", "rencontres d'auteurs régulières", "sélection large (littérature, polar, essais, jeunesse, BD)"])
append_source(5, "Enrichissement WebSearch : note '5.0/5 sur 74 avis web' trouvée mais source non identifiée comme Google Maps (agrégateur générique) — jugée non fiable, NON ajoutée en note_google conformément à la règle vérifié/agrégé.")

# --- id 6 : Chaleur ---
append_source(6, "Tentative d'enrichissement WebSearch (à propos/avis) : la recherche sur l'adresse 67 Bd Chave remonte principalement 'Bouillon' et 'Bistrot Chave' (établissements distincts et voisins sur le même boulevard), pas d'information fiable spécifique à Chaleur trouvée cette fois-ci. Aucune donnée ajoutée.")

# --- id 7 : Sassy — VÉRIFIÉ via fetch direct restaurants-de-france.fr ---
cur.execute("UPDATE lieux SET note_google = ?, nombre_avis_google = ? WHERE id = ?", (4.6, 85, 7))
add_services(7, ["Bar disponible sur place", "Toilettes", "Wifi", "Terrasse", "Vente à emporter", "Livraison", "Accessible en fauteuil roulant"])
add_tags(7, ["ambiance décontractée", "cadre agréable", "chiens acceptés", "groupes et touristes bienvenus", "excellents cocktails", "excellent café", "grand choix de vins", "réservations acceptées", "produits frais et de saison"])
append_source(7, "VÉRIFIÉ via fetch direct restaurants-de-france.fr (fiche synchronisée Google Maps, MAJ 18/11/2025) : note 4.6/5 sur 85 avis. Bloc 'à propos' complet extrait (accessibilité, ambiance, animaux, clientèle, offre, paiements, planning, points forts, populaire pour, services, services de restauration/disponibles).")

# --- id 8 : Mauvaise Herbe ---
add_tags(8, ["cuisine végétale méditerranéenne", "ambiance chaleureuse", "design épuré et minimaliste", "ouvert 7j/7", "plats colorés faits maison"])
append_source(8, "Enrichissement WebSearch : restaurant vegan, cuisine méditerranéenne/bistro décontractée, bons retours sur le service et l'ambiance. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 9 : Le Magnolia ---
add_tags(9, ["cuisine fusion franco-asiatique", "terrasse ombragée", "grand choix de cocktails et spiritueux", "ambiance festive", "bo-buns et curry de légumes réputés"])
append_source(9, "Enrichissement WebSearch : notes agrégées trouvées hors Google (TheFork 9.0/10 sur 280 avis ; Tripadvisor 4.5/5) — non reportées en note_google (champ réservé aux notes Google vérifiées/agrégées Google), gardées ici à titre indicatif uniquement.")

# --- id 10 : Road Social Club ---
add_services(10, ["Salle de sport", "Cours de yoga/pilates", "Restauration sur place"])
add_tags(10, ["concept café + sport + bien-être", "espace inclusif et sécurisant", "événements bien-être réguliers", "deux studios (Flow détente / Training intense)"])
append_source(10, "Enrichissement WebSearch : concept hybride café/salle de sport/bien-être ouvert automne 2025. Aucune note Google chiffrée trouvée — non ajoutée.")

con.commit()
cur.execute("SELECT id, nom, note_google, nombre_avis_google FROM lieux WHERE id BETWEEN 1 AND 10 ORDER BY id")
for r in cur.fetchall(): print(r)
con.close()
print("OK batch 1")
