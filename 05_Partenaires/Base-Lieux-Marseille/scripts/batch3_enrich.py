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

# --- id 21 : Mat'cha ---
add_tags(21, ["bubble tea et matcha lattes artisanaux (perles maison, matcha bio du Japon)", "petit espace cosy aux couleurs apaisantes", "accueil chaleureux, service rapide"])
append_source(21, "Enrichissement WebSearch : bubble tea/matcha shop tenu par Anthony depuis avril 2023 près du Cours Julien. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 22 : Polpette ---
add_tags(22, ["trattoria italo-marseillaise pur jus", "pinsa et polpettes de bœuf signature", "tapas le soir", "terrasse en cours de rénovation (2026)", "vue sur Saint-Victor et le Vieux-Port"])
append_source(22, "Enrichissement WebSearch : trattoria/aperitivo au pied de l'abbaye Saint-Victor. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 23 : Black Bird Coffee — VÉRIFIÉ via fetch direct restaurants-de-france.fr ---
cur.execute("UPDATE lieux SET note_google = ?, nombre_avis_google = ? WHERE id = ?", (4.6, 705, 23))
add_services(23, ["Toilettes", "Wifi", "Bar disponible sur place", "Terrasse", "Vente à emporter", "Livraison", "Parking accessible en fauteuil roulant"])
add_tags(23, ["ambiance décontractée et branchée", "adapté au travail sur ordinateur portable", "convient aux végétariens/véganes", "excellent café et desserts", "grand choix de thés et bières", "grande terrasse ombragée", "brunch du dimanche réputé"])
append_source(23, "VÉRIFIÉ via fetch direct restaurants-de-france.fr (fiche synchronisée Google Maps, MAJ 25/11/2025) : note 4.6/5 sur 705 avis. Bloc 'à propos' complet extrait.")

# --- id 24 : Lala Café ---
add_services(24, ["Boutique engagée"])
add_tags(24, ["café-cantine méditerranéenne + boutique engagée", "café colombien torréfié rue Saint-Pierre (Marseille)", "mobilier artisanal local (tabourets tuftés par l'artiste Liso)", "ambiance chaleureuse et organique"])
append_source(24, "Enrichissement WebSearch : lieu hybride café/cantine/boutique solidaire récemment ouvert (quartier Plaine). Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 25 : Risette ---
append_source(25, "Tentative d'enrichissement WebSearch (à propos/avis) : aucune information fiable trouvée pour 'Risette' au 37 rue Vacon (résultats renvoyant d'autres commerces de la rue). Aucune donnée ajoutée — à réinvestiguer ultérieurement si besoin.")

# --- id 26 : La Fiancée ---
add_tags(26, ["décor industriel épuré (bois + métal)", "brunch réputé, cuisine généreuse et équilibrée", "café jugé excellent", "avis contrastés sur l'accueil/le service selon les visites"])
append_source(26, "Enrichissement WebSearch : brunch café reconnu pour sa cuisine mais avis partagés sur le service/l'accueil selon les retours — reflété fidèlement sans lisser. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 27 : Fyne Urban Kahwa — VÉRIFIÉ via fetch direct restaurants-de-france.fr + site officiel ---
cur.execute("UPDATE lieux SET note_google = ?, nombre_avis_google = ?, telephone_public = ? WHERE id = ?", (4.7, 471, "07 72 05 70 57", 27))
add_services(27, ["Toilettes", "Terrasse", "Vente à emporter", "Livraison", "Salle à manger privée"])
add_tags(27, ["accessible en fauteuil roulant", "chiens acceptés (intérieur et extérieur)", "LGBTQ+ friendly", "safe place personnes trans", "établissement géré par une femme", "plats halal, bio, végétaliens disponibles", "happy hour sur boissons et restauration", "excellent café", "avis clients très contrastés sur la régularité de la cuisine (qualité fluctuante selon les visites)"])
append_source(27, "VÉRIFIÉ via fetch direct restaurants-de-france.fr (fiche synchronisée Google Maps, MAJ 13/10/2025) : note 4.7/5 sur 471 avis. Bloc 'à propos' riche (accessibilité, LGBTQ+/trans safe place, géré par une femme, halal/bio/vegan). RÉSOLUTION de l'item ouvert 'numéro caché derrière un bouton JS' : le numéro +33 7 72 05 70 57 (07 72 05 70 57) a été retrouvé en clair dans le footer du site officiel (lien tel: dans le code de la page) — ajouté à la fiche.")

# --- id 28 : Maison Bahja ---
add_tags(28, ["Kahwa shop marocain haut de gamme", "ambiance orient/occident, bancs béton inspirés Le Corbusier", "cornes de gazelle et macarons colorés", "thés royaux fleur d'oranger et miel"])
append_source(28, "Enrichissement WebSearch : Kahwashop marocain de luxe, ouvert récemment rue de la République. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 29 : Voilà Vé ---
add_tags(29, ["bar à vins bio/biodynamiques/nature exclusivement", "déco art déco chaleureuse (bougies, guirlandes lumineuses)", "long espace avec patio paisible caché à l'arrière", "planches charcuterie pyrénéenne et fromages fermiers"])
append_source(29, "Enrichissement WebSearch : bar à vin nature du Camas, cadre vintage soigné. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 30 : Pétrin Couchette ---
add_services(30, ["Terrasse"])
add_tags(30, ["boulangerie/café au levain naturel", "pains variés (campagne, épeautre, khorasan, riz-sarrasin)", "terrasse ~60 places sur petite place animée", "labellisé 3 Ecotables (engagement durable)"])
append_source(30, "Enrichissement WebSearch : boulangerie-café ouverte avril 2022, ancrage engagement durable (3 Ecotables). Aucune note Google chiffrée trouvée — non ajoutée.")

con.commit()
cur.execute("SELECT id, nom, note_google, nombre_avis_google, telephone_public FROM lieux WHERE id BETWEEN 21 AND 30 ORDER BY id")
for r in cur.fetchall(): print(r)
con.close()
print("OK batch 3")
