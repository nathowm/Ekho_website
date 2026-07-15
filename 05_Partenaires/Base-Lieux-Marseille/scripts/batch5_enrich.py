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

# --- id 39 : Maurice ---
append_source(39, "Tentative d'enrichissement WebSearch (à propos/avis) : aucune information fiable trouvée pour 'Maurice' au 76 rue de Lodi (résultats renvoyant un établissement voisin différent, La Ciergerie au n°8). Aucune donnée ajoutée.")

# --- id 40 : Les Babines de Mars ---
add_services(40, ["Terrasse"])
add_tags(40, ["a succédé au restaurant Les Eaux de Mars (même esprit bistrot, équipe quasi identique)", "chef formé Ferrandi (Igor de Prittwitz)", "cuisine créative de saison, assiettes à partager le soir", "ambiance conviviale et moderne, cocktails originaux", "labellisé Ecotable"])
append_source(40, "Enrichissement WebSearch : bistronomie de saison, reprise des Eaux de Mars. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 41 : Yuzu Record Bar ---
add_services(41, ["Galerie d'art", "Programmation musicale (DJ sets, concerts)"])
add_tags(41, ["bar audiophile à système son haut de gamme", "tapas méditerranéennes et cocktails signature", "expositions d'art tournantes", "programmation éclectique (jazz, électro, soul, world)", "ambiance cosmopolite et marseillaise à Noailles"])
append_source(41, "Enrichissement WebSearch : hybride bar à vin/restaurant/espace musical/galerie à Noailles, ouverture récente. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 42 : Grand Écart ---
add_services(42, ["Studio de sport", "Cave à vins nature"])
add_tags(42, ["concept hybride studio sport + café spécialité + cantine + cave à vins nature", "terrasse, ambiance cosy et bohème type Cours Julien", "playlists variées (calme le matin, festif le soir)", "coachs motivants selon les avis"])
append_source(42, "Enrichissement WebSearch : lieu hybride sport/café/vin nature. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 43 : 7VB Café ---
add_tags(43, ["café de spécialité + cuisine franco-américaine maison", "cinnamon rolls réputés", "ambiance cosy sans être bondée, équipe bilingue", "quartier du Panier"])
append_source(43, "Enrichissement WebSearch : café de spécialité réputé du Panier, ~849 avis mentionnés sur une page restaurants-de-france.fr en fragment de recherche mais sans note chiffrée exploitable ni URL directe confirmée — non ajouté en note_google pour éviter toute donnée non vérifiée.")

# --- id 44 : Chez Moe ---
cur.execute("UPDATE lieux SET note_google = ? WHERE id = ?", (4.9, 44))
add_tags(44, ["coffee shop le jour / bar à vin nature le soir", "design bois clair, esthétique Tokyo x Stockholm", "accueil chaleureux et passionné (patron Moe)", "café de spécialité (Brûlerie Möka), matcha glacé, vins natures"])
append_source(44, "Note Google 4.9 mentionnée explicitement comme telle par la source WebSearch agrégée (sans fetch direct d'une fiche Google Maps synchronisée) — reportée en note_google mais flaguée AGRÉGÉE/non vérifiée par fetch direct. Nombre d'avis non trouvé.")

# --- id 45 : Maison Nosh ---
add_tags(45, ["coffee shop + brunch (enseigne aixoise étendue à Marseille)", "ambiance chaleureuse, moderne, lumineuse, kids friendly", "propice au télétravail", "cadre méditerranéen place aux Huiles"])
append_source(45, "Enrichissement WebSearch : note '5.0/5' trouvée mais sur Tripadvisor, PAS Google — non reportée en note_google (règle : uniquement notes Google /5).")

# --- id 46 : Pain Salvator ---
cur.execute("UPDATE lieux SET note_google = ? WHERE id = ?", (4.6, 46))
add_tags(46, ["boulangerie au levain naturel bio/local", "ambiance comptoir + café conviviale", "petits bancs sur trottoir près des fours", "offre végétarienne/vegan"])
append_source(46, "Note Google 4.6 mentionnée explicitement comme telle par la source WebSearch agrégée (sans fetch direct d'une fiche Google Maps synchronisée) — reportée en note_google mais flaguée AGRÉGÉE/non vérifiée par fetch direct. Nombre d'avis non trouvé.")

# --- id 47 : La Caravelle ---
add_tags(47, ["bar/restaurant historique depuis les années 1920, lieu emblématique d'artistes/voyageurs", "concerts jazz et black music mercredi et vendredi (octobre-mai)", "vue imprenable sur le Vieux-Port et Notre-Dame-de-la-Garde", "cuisine provençale (daube, tripes, aïoli, anchoïade)"])
append_source(47, "Enrichissement WebSearch : note '9.2/10' trouvée mais sur TheFork, PAS Google — non reportée en note_google.")

# --- id 48 : John Silver ---
add_tags(48, ["premier « bistroffee » 100% végétal de Marseille", "petit espace (18-20 couverts), déco tables rondes pieds fonte", "accueil chaleureux et énergie positive selon les avis"])
append_source(48, "Enrichissement WebSearch : bistrot-coffee shop 100% végétal près du Vieux-Port. Aucune note Google chiffrée trouvée — non ajoutée.")

# --- id 49 : Ivresse ---
add_services(49, ["Cave à vins"])
add_tags(49, ["cave à vins nature (sans sulfites ajoutés) + restaurant", "ancien garage réhabilité, ambiance bougies et murs bruts", "plats locavores et de saison (poisson fumé, betteraves rôties)", "service parfois jugé long selon certains avis"])
append_source(49, "Enrichissement WebSearch : cave à vins nature / restaurant près du Parc Longchamp. Aucune note Google chiffrée trouvée — non ajoutée.")

con.commit()
cur.execute("SELECT id, nom, note_google, nombre_avis_google FROM lieux WHERE id BETWEEN 39 AND 49 ORDER BY id")
for r in cur.fetchall(): print(r)
con.close()
print("OK batch 5")
