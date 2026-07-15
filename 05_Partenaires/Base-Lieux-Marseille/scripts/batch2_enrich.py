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

# --- id 11 : Da-yé ---
append_source(11, "Tentative d'enrichissement WebSearch (à propos/avis) : aucune fiche fiable trouvée pour '22 Boulevard Louis Salvator' (résultats non pertinents). Aucune donnée ajoutée.")

# --- id 12 : Le Trois Quarts ---
add_tags(12, ["ancien bar-troquet réhabilité (comptoir historique conservé)", "équipe jeune et ambiance décontractée", "bière locale et vin bio", "planche fruits de mer réputée", "portions jugées petites pour le prix"])
append_source(12, "Note 4.2/5 sur 54 avis trouvée via WebSearch agrégé (Yelp/Tripadvisor/Marseille Tourisme) — source non confirmée comme fiche Google Maps synchronisée, donc NON reportée en note_google (règle vérifié/agrégé).")

# --- id 13 : Au Jardin ---
add_tags(13, ["salon de thé et épicerie bio", "cour arborée et ombragée (petite oasis en ville)", "pâtisseries maison 100% bio (sans gluten possible)", "tables dépareillées, ambiance détente"])
append_source(13, "Enrichissement WebSearch : salon de thé bio repris début 2023, ambiance conviviale de quartier. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 14 : APT.20 ---
add_tags(14, ["coffee shop inspiré de New York / clin d'œil à Friends (Monica's apartment)", "canapés chesterfield, déco diner américain", "DJ sets, pop-up tattoo, running club", "cold brew et cookies réputés"])
append_source(14, "Enrichissement WebSearch : coffee shop concept NYC très suivi sur les réseaux (TikTok/Instagram). Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 15 : Silk ---
add_tags(15, ["concept hybride café + friperie vintage", "brunch et petite restauration soignée", "sélection de vêtements vintage pointue"])
append_source(15, "Enrichissement WebSearch : hybride coffee shop/restauration créative/vintage. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 16 : Le 68 — VÉRIFIÉ via fetch direct restaurants-de-france.fr ---
cur.execute("UPDATE lieux SET note_google = ?, nombre_avis_google = ? WHERE id = ?", (4.2, 306, 16))
add_services(16, ["Bar disponible sur place", "Toilettes", "Terrasse", "Vente à emporter", "Livraison"])
add_tags(16, ["ambiance décontractée et calme", "cuisine méditerranéenne, poisson grillé et pâtes fraîches", "salade caesar créative", "épicerie fine sur place", "avis clients contrastés sur l'accueil selon les périodes"])
append_source(16, "VÉRIFIÉ via fetch direct restaurants-de-france.fr (fiche synchronisée Google Maps, MAJ 18/11/2025) : note 4.2/5 sur 306 avis. Bloc 'à propos' complet extrait. NB : avis récents contrastés (plusieurs avis 1/5 sur accueil/gestion addition pour un grand groupe, à côté d'avis très positifs) — reflété fidèlement, ni minimisé ni amplifié.")

# --- id 17 : Café Pollux ---
add_tags(17, ["ambiance cosy et paisible (pas d'ordinateurs, esprit décrocher)", "bar carrelé, déco chinée, murs à photos", "pâtisseries maison réputées (carrot cake)", "spécialités café (matcha lait d'avoine, flat white)"])
append_source(17, "Enrichissement WebSearch : note '8.8/10 sur 654 avis' trouvée mais sur une échelle /10 non caractéristique de Google (probablement TheFork ou agrégateur) — NON reportée en note_google conformément à la règle vérifié/agrégé (uniquement notes Google /5).")

# --- id 18 : Pulse Café ---
add_services(18, ["Studio yoga/pilates", "Boutique créateurs"])
add_tags(18, ["concept café-cantine + boutique + studio yoga/pilates", "salle lumineuse vue Palais Longchamp", "terrasse ensoleillée", "cookies matcha et lattes réputés"])
append_source(18, "Enrichissement WebSearch : concept bien-être/café/boutique près du Palais Longchamp. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 19 : Café LaMuse — VÉRIFIÉ via fetch direct restaurants-de-france.fr ---
cur.execute("UPDATE lieux SET note_google = ?, nombre_avis_google = ? WHERE id = ?", (4.3, 629, 19))
add_services(19, ["Bar disponible sur place", "Toilettes", "Toilettes non genrées", "Wifi", "Terrasse", "Livraison"])
add_tags(19, ["accessible en fauteuil roulant", "ambiance décontractée et branchée", "chiens acceptés", "LGBTQ+ friendly", "safe place personnes trans", "adapté aux familles (chaises hautes, menu enfant)", "excellent café", "grand choix de bières et vins", "service tard en soirée"])
append_source(19, "VÉRIFIÉ via fetch direct restaurants-de-france.fr (fiche synchronisée Google Maps, MAJ 25/11/2025) : note 4.3/5 sur 629 avis. Bloc 'à propos' complet extrait (accessibilité, clientèle LGBTQ+/familles, offre, services).")

# --- id 20 : Le Poulpe (Saint-Victor) ---
add_tags(20, ["vue panoramique sur le Vieux-Port, l'Abbaye Saint-Victor et le MuCEM", "spot apéritif au coucher du soleil", "tapas de la mer (poulpe mariné signature)", "ambiance paisible en terrasse"])
append_source(20, "Enrichissement WebSearch : attention, une fiche restaurants-de-france.fr existe pour un établissement homonyme 'Le Poulpe' au 84 Quai du Port (13002) — adresse DIFFÉRENTE de notre lieu (1 Place Saint-Victor, 13007) : donnée non utilisée pour éviter toute confusion entre deux établissements distincts. Note Google '4' mentionnée de façon vague via WebSearch sans décimale ni source claire — non ajoutée en note_google.")

con.commit()
cur.execute("SELECT id, nom, note_google, nombre_avis_google FROM lieux WHERE id BETWEEN 11 AND 20 ORDER BY id")
for r in cur.fetchall(): print(r)
con.close()
print("OK batch 2")
