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

# --- id 31 : Vorace — VÉRIFIÉ via fetch direct restaurants-de-france.fr ---
cur.execute("UPDATE lieux SET note_google = ?, nombre_avis_google = ? WHERE id = ?", (4.8, 146, 31))
add_services(31, ["Bar disponible sur place", "Toilettes", "Terrasse", "Vente à emporter", "Livraison"])
add_tags(31, ["ambiance décontractée et branchée", "carte renouvelée régulièrement (produits frais et de saison)", "sélection de vins régionaux et internationaux", "excellents cocktails et grand choix de vins"])
append_source(31, "VÉRIFIÉ via fetch direct restaurants-de-france.fr (fiche synchronisée Google Maps, MAJ 19/11/2025) : note 4.8/5 sur 146 avis. Bloc 'à propos' complet extrait.")

# --- id 32 : Mon Gâté ---
add_tags(32, ["salon de thé spécialisé choux à la crème (sucrés/salés)", "décoration soignée, ambiance propre et chaleureuse", "plats salés faits maison au déjeuner"])
append_source(32, "Enrichissement WebSearch : note '4.9/5' trouvée mais sur Tripadvisor, PAS Google — non reportée en note_google (règle : uniquement notes Google /5, vérifiées ou clairement identifiées comme telles).")

# --- id 33 : Josie ---
add_services(33, ["Ateliers créatifs"])
add_tags(33, ["café de spécialité + ateliers créatifs", "petit-déjeuner toute la journée", "ambiance lumineuse et conviviale", "sourcing local"])
append_source(33, "Enrichissement WebSearch : coffee shop récent proposant aussi des ateliers créatifs (rue de Bruys, Camas). Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 34 : Brûlerie Möka ---
cur.execute("UPDATE lieux SET note_google = ? WHERE id = ?", (4.7, 34))
add_tags(34, ["torréfacteur de café de quartier engagé/éthique", "décoration vintage chinée (chaises dépareillées, machine Faema)", "espace extérieur cosy et décontracté", "chai latte, matcha, pâtisseries maison réputés"])
append_source(34, "Note Google 4.7 mentionnée explicitement comme telle par la source WebSearch agrégée (sans fetch direct d'une fiche Google Maps synchronisée) — reportée en note_google mais flaguée AGRÉGÉE/non vérifiée par fetch direct, conformément à la règle vérifié/agrégé. Nombre d'avis non trouvé.")

# --- id 35 : Le Petit Café ---
add_tags(35, ["café de quartier ouvert en semaine uniquement", "ambiance conviviale, patron chaleureux", "formule petit-déjeuner"])
append_source(35, "Enrichissement WebSearch : petit café de quartier place de la Corderie, ambiance de repaire local. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 36 : Mañana ---
append_source(36, "Tentative d'enrichissement WebSearch (à propos/avis) : aucune information fiable trouvée spécifiquement pour 'Mañana' au 120 boulevard de la Corderie (résultats renvoyant un établissement voisin différent, Brasserie Le Saint Victor). Aucune donnée ajoutée.")

con.commit()
cur.execute("SELECT id, nom, note_google, nombre_avis_google FROM lieux WHERE id BETWEEN 31 AND 36 ORDER BY id")
for r in cur.fetchall(): print(r)
con.close()
print("OK batch 4")
