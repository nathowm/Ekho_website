import sqlite3
from datetime import date

con = sqlite3.connect('lieux_mirror.db')
cur = con.cursor()
today = date.today().isoformat()

def get_or_create(table, nom):
    cur.execute(f"INSERT OR IGNORE INTO {table} (nom) VALUES (?)", (nom,))
    cur.execute(f"SELECT id FROM {table} WHERE nom = ?", (nom,))
    return cur.fetchone()[0]

def unlink_tag(lieu_id, tag_nom):
    cur.execute("SELECT id FROM tags WHERE nom = ?", (tag_nom,))
    row = cur.fetchone()
    if not row:
        print(f"  [WARN] tag introuvable pour id {lieu_id}: {tag_nom!r}")
        return
    tid = row[0]
    cur.execute("DELETE FROM lieu_tags WHERE lieu_id = ? AND tag_id = ?", (lieu_id, tid))

def add_service(lieu_id, service_nom):
    sid = get_or_create('services', service_nom)
    cur.execute("INSERT OR IGNORE INTO lieu_services (lieu_id, service_id) VALUES (?,?)", (lieu_id, sid))

def rename_tag(old_nom, new_nom):
    # Only rename if new_nom not already an existing distinct tag; else merge (move links then delete old)
    cur.execute("SELECT id FROM tags WHERE nom = ?", (old_nom,))
    old_row = cur.fetchone()
    if not old_row:
        print(f"  [WARN] tag à renommer introuvable: {old_nom!r}")
        return
    old_id = old_row[0]
    cur.execute("SELECT id FROM tags WHERE nom = ?", (new_nom,))
    new_row = cur.fetchone()
    if new_row and new_row[0] != old_id:
        new_id = new_row[0]
        # merge: repoint lieu_tags from old_id to new_id, ignore dupes
        cur.execute("SELECT lieu_id FROM lieu_tags WHERE tag_id = ?", (old_id,))
        for (lid,) in cur.fetchall():
            cur.execute("INSERT OR IGNORE INTO lieu_tags (lieu_id, tag_id) VALUES (?,?)", (lid, new_id))
        cur.execute("DELETE FROM lieu_tags WHERE tag_id = ?", (old_id,))
    else:
        cur.execute("UPDATE tags SET nom = ? WHERE id = ?", (new_nom, old_id))

def append_source(lieu_id, note):
    cur.execute("SELECT source_donnees FROM lieux WHERE id = ?", (lieu_id,))
    (existing,) = cur.fetchone()
    existing = existing or ""
    new = existing + (f"\n[{today}] {note}" if existing else f"[{today}] {note}")
    cur.execute("UPDATE lieux SET source_donnees = ? WHERE id = ?", (new, lieu_id))

PLAN = {
 1: {
   'drop': ["décoration japonaise raffinée", "ambiance minimaliste et élégante", "cheesecakes japonais légers"],
 },
 2: {
   'drop': ["café-galerie hybride et solidaire", "ambiance chaleureuse et détendue", "spécialités maghrébines (eau de rose, tahini latte)"],
 },
 3: {
   'drop': ["desserts maison", "ambiance conviviale quartier Camas", "terrasse animée", "options végétariennes copieuses"],
   'services': ["Options végétariennes/véganes"],
 },
 4: {
   'drop': ["ambiance conviviale quartier", "peut être exigu aux heures d'affluence"],
   'rename': {"soirées à thème (poker lundi, DJ vendredi, foot/rugby)": "Soirées à thème (poker, DJ, foot/rugby)"},
 },
 5: {
   'drop': ["librairie-café", "ambiance lumineuse et conviviale", "sélection large (littérature, polar, essais, jeunesse, BD)"],
 },
 7: {
   'drop': ["ambiance décontractée", "cadre agréable", "chiens acceptés", "groupes et touristes bienvenus", "réservations acceptées", "produits frais et de saison"],
   'services': ["Chiens acceptés", "Réservations acceptées"],
 },
 8: {
   'drop': ["cuisine végétale méditerranéenne", "ambiance chaleureuse", "design épuré et minimaliste", "ouvert 7j/7", "plats colorés faits maison"],
 },
 9: {
   'drop': ["cuisine fusion franco-asiatique", "terrasse ombragée", "ambiance festive"],
   'rename': {"grand choix de cocktails et spiritueux": "Grand choix de cocktails et spiritueux"},
 },
 10: {
   'drop': ["concept café + sport + bien-être"],
 },
 12: {
   'drop': ["équipe jeune et ambiance décontractée", "portions jugées petites pour le prix"],
   'rename': {"ancien bar-troquet réhabilité (comptoir historique conservé)": "Ancien bar-troquet réhabilité (comptoir d'origine)",
              "bière locale et vin bio": "Bière locale et vin bio"},
 },
 13: {
   'drop': ["salon de thé et épicerie bio", "tables dépareillées, ambiance détente"],
   'rename': {"cour arborée et ombragée (petite oasis en ville)": "Cour arborée et ombragée",
              "pâtisseries maison 100% bio (sans gluten possible)": "Pâtisseries maison bio (sans gluten possible)"},
 },
 14: {
   'rename': {"coffee shop inspiré de New York / clin d'œil à Friends (Monica's apartment)": "Inspiré de l'appart de Monica (Friends)",
              "canapés chesterfield, déco diner américain": "Déco diner américain, canapés chesterfield"},
 },
 15: {
   'drop': ["concept hybride café + friperie vintage", "brunch et petite restauration soignée"],
   'rename': {"sélection de vêtements vintage pointue": "Sélection vintage pointue"},
 },
 16: {
   'drop': ["ambiance décontractée et calme", "épicerie fine sur place", "avis clients contrastés sur l'accueil selon les périodes"],
   'rename': {"cuisine méditerranéenne, poisson grillé et pâtes fraîches": "Poisson grillé et pâtes fraîches"},
 },
 17: {
   'drop': ["spécialités café (matcha lait d'avoine, flat white)"],
   'rename': {"ambiance cosy et paisible (pas d'ordinateurs, esprit décrocher)": "Ambiance cosy, esprit déconnexion (pas d'ordinateurs)",
              "bar carrelé, déco chinée, murs à photos": "Déco chinée, bar carrelé, murs à photos",
              "pâtisseries maison réputées (carrot cake)": "Carrot cake et pâtisseries maison réputées"},
 },
 18: {
   'drop': ["concept café-cantine + boutique + studio yoga/pilates", "terrasse ensoleillée"],
   'services': ["Terrasse"],
   'rename': {"salle lumineuse vue Palais Longchamp": "Vue sur le Palais Longchamp",
              "cookies matcha et lattes réputés": "Cookies matcha et lattes réputés"},
 },
 19: {
   'drop': ["ambiance décontractée et branchée", "accessible en fauteuil roulant", "chiens acceptés", "LGBTQ+ friendly",
            "safe place personnes trans", "adapté aux familles (chaises hautes, menu enfant)", "service tard en soirée"],
   'services': ["Accessible en fauteuil roulant", "Chiens acceptés", "LGBTQ+ friendly", "Safe place personnes trans",
                "Adapté aux familles", "Service tard en soirée"],
 },
 20: {
   'drop': ["ambiance paisible en terrasse"],
   'rename': {"vue panoramique sur le Vieux-Port, l'Abbaye Saint-Victor et le MuCEM": "Vue panoramique Vieux-Port / Saint-Victor / MuCEM",
              "spot apéritif au coucher du soleil": "Spot apéritif au coucher du soleil",
              "tapas de la mer (poulpe mariné signature)": "Poulpe mariné signature"},
 },
 21: {
   'drop': ["bubble tea et matcha lattes artisanaux (perles maison, matcha bio du Japon)", "petit espace cosy aux couleurs apaisantes", "accueil chaleureux, service rapide"],
 },
 22: {
   'drop': ["trattoria italo-marseillaise pur jus", "tapas le soir", "terrasse en cours de rénovation (2026)"],
   'rename': {"vue sur Saint-Victor et le Vieux-Port": "Vue sur Saint-Victor et le Vieux-Port"},
 },
 23: {
   'drop': ["ambiance décontractée et branchée", "adapté au travail sur ordinateur portable", "convient aux végétariens/véganes", "grande terrasse ombragée"],
   'services': ["Adapté au travail sur ordinateur", "Options végétariennes/véganes"],
   'rename': {"excellent café et desserts": "Excellent café et desserts"},
 },
 24: {
   'drop': ["café-cantine méditerranéenne + boutique engagée", "ambiance chaleureuse et organique"],
   'rename': {"café colombien torréfié rue Saint-Pierre (Marseille)": "Café colombien torréfié à Marseille",
              "mobilier artisanal local (tabourets tuftés par l'artiste Liso)": "Mobilier artisanal local (tabourets par l'artiste Liso)"},
 },
 26: {
   'drop': ["café jugé excellent", "avis contrastés sur l'accueil/le service selon les visites"],
   'rename': {"décor industriel épuré (bois + métal)": "Décor industriel épuré (bois + métal)",
              "brunch réputé, cuisine généreuse et équilibrée": "Brunch réputé"},
 },
 27: {
   'drop': ["accessible en fauteuil roulant", "chiens acceptés (intérieur et extérieur)", "LGBTQ+ friendly", "safe place personnes trans",
            "établissement géré par une femme", "plats halal, bio, végétaliens disponibles", "happy hour sur boissons et restauration",
            "avis clients très contrastés sur la régularité de la cuisine (qualité fluctuante selon les visites)"],
   'services': ["Accessible en fauteuil roulant", "Chiens acceptés", "LGBTQ+ friendly", "Safe place personnes trans",
                "Géré par une femme", "Plats halal", "Plats bio", "Plats végétaliens", "Happy hour"],
 },
 28: {
   'drop': ["Kahwa shop marocain haut de gamme"],
   'rename': {"ambiance orient/occident, bancs béton inspirés Le Corbusier": "Bancs béton inspirés Le Corbusier, ambiance orient/occident"},
 },
 29: {
   'drop': ["bar à vins bio/biodynamiques/nature exclusivement"],
   'rename': {"déco art déco chaleureuse (bougies, guirlandes lumineuses)": "Déco art déco (bougies, guirlandes lumineuses)",
              "long espace avec patio paisible caché à l'arrière": "Patio caché à l'arrière"},
 },
 30: {
   'drop': ["boulangerie/café au levain naturel", "terrasse ~60 places sur petite place animée"],
   'rename': {"pains variés (campagne, épeautre, khorasan, riz-sarrasin)": "Pains variés (campagne, épeautre, khorasan...)",
              "labellisé 3 Ecotables (engagement durable)": "Labellisé 3 Ecotables"},
 },
 31: {
   'drop': ["ambiance décontractée et branchée", "carte renouvelée régulièrement (produits frais et de saison)", "sélection de vins régionaux et internationaux"],
   'rename': {"excellents cocktails et grand choix de vins": "Excellents cocktails et grand choix de vins"},
 },
 32: {
   'drop': ["salon de thé spécialisé choux à la crème (sucrés/salés)", "décoration soignée, ambiance propre et chaleureuse"],
   'rename': {"plats salés faits maison au déjeuner": "Plats salés maison au déjeuner"},
 },
 33: {
   'drop': ["café de spécialité + ateliers créatifs", "ambiance lumineuse et conviviale", "sourcing local"],
 },
 34: {
   'drop': ["torréfacteur de café de quartier engagé/éthique", "espace extérieur cosy et décontracté"],
   'rename': {"décoration vintage chinée (chaises dépareillées, machine Faema)": "Déco vintage chinée (machine Faema)",
              "chai latte, matcha, pâtisseries maison réputés": "Chai latte, matcha et pâtisseries maison réputés"},
 },
 35: {
   'drop': ["café de quartier ouvert en semaine uniquement", "ambiance conviviale, patron chaleureux", "formule petit-déjeuner"],
 },
 40: {
   'drop': ["cuisine créative de saison, assiettes à partager le soir", "ambiance conviviale et moderne, cocktails originaux"],
   'rename': {"a succédé au restaurant Les Eaux de Mars (même esprit bistrot, équipe quasi identique)": "A succédé aux Eaux de Mars (même esprit, équipe quasi identique)",
              "chef formé Ferrandi (Igor de Prittwitz)": "Chef formé Ferrandi (Igor de Prittwitz)"},
 },
 41: {
   'drop': ["bar audiophile à système son haut de gamme", "tapas méditerranéennes et cocktails signature", "expositions d'art tournantes", "ambiance cosmopolite et marseillaise à Noailles"],
   'rename': {"programmation éclectique (jazz, électro, soul, world)": "Programmation éclectique (jazz, électro, soul, world)"},
 },
 42: {
   'drop': ["concept hybride studio sport + café spécialité + cantine + cave à vins nature", "terrasse, ambiance cosy et bohème type Cours Julien", "playlists variées (calme le matin, festif le soir)", "coachs motivants selon les avis"],
   'services': ["Terrasse"],
 },
 43: {
   'drop': ["café de spécialité + cuisine franco-américaine maison", "quartier du Panier"],
   'rename': {"cinnamon rolls réputés": "Cinnamon rolls réputés",
              "ambiance cosy sans être bondée, équipe bilingue": "Ambiance cosy, équipe bilingue"},
 },
 44: {
   'drop': ["accueil chaleureux et passionné (patron Moe)", "café de spécialité (Brûlerie Möka), matcha glacé, vins natures"],
   'rename': {"design bois clair, esthétique Tokyo x Stockholm": "Design bois clair, esthétique Tokyo x Stockholm"},
 },
 45: {
   'drop': ["ambiance chaleureuse, moderne, lumineuse, kids friendly", "propice au télétravail", "cadre méditerranéen place aux Huiles"],
   'services': ["Adapté aux familles", "Adapté au télétravail"],
   'rename': {"coffee shop + brunch (enseigne aixoise étendue à Marseille)": "Enseigne aixoise reconnue, étendue à Marseille"},
 },
 46: {
   'drop': ["boulangerie au levain naturel bio/local", "ambiance comptoir + café conviviale", "offre végétarienne/vegan"],
   'services': ["Options végétariennes/véganes"],
   'rename': {"petits bancs sur trottoir près des fours": "Petits bancs sur le trottoir près des fours"},
 },
 47: {
   'drop': ["concerts jazz et black music mercredi et vendredi (octobre-mai)"],
   'rename': {"bar/restaurant historique depuis les années 1920, lieu emblématique d'artistes/voyageurs": "Historique depuis les années 1920, lieu emblématique d'artistes/voyageurs",
              "cuisine provençale (daube, tripes, aïoli, anchoïade)": "Cuisine provençale (daube, tripes, aïoli, anchoïade)"},
 },
 48: {
   'drop': ["accueil chaleureux et énergie positive selon les avis"],
   'rename': {"petit espace (18-20 couverts), déco tables rondes pieds fonte": "Petit espace (18-20 couverts), tables rondes pieds fonte"},
 },
 49: {
   'drop': ["cave à vins nature (sans sulfites ajoutés) + restaurant", "service parfois jugé long selon certains avis"],
   'rename': {"ancien garage réhabilité, ambiance bougies et murs bruts": "Ancien garage réhabilité, ambiance bougies et murs bruts",
              "plats locavores et de saison (poisson fumé, betteraves rôties)": "Plats locavores et de saison (poisson fumé, betteraves rôties)"},
 },
 51: {
   'drop': ["ambiance brute/atelier, jeune équipe visible aux fours", "file d'attente fréquente le matin"],
   'rename': {"boulangerie de quartier bio, devanture jaune vif reconnaissable": "Devanture jaune vif reconnaissable",
              "focaccia, pizza, croissants et cinnamon rolls faits maison chaque jour": "Focaccia, pizza, croissants, cinnamon rolls faits maison"},
 },
 52: {
   'drop': ["salle de concert intimiste au Cours Julien", "programmation musicale éclectique plusieurs soirs par semaine", "ambiance conviviale, personnel apprécié"],
   'rename': {"large choix de bières (bouteilles du monde + pression)": "Large choix de bières (bouteilles du monde + pression)"},
 },
 53: {
   'drop': ["accessible en fauteuil roulant", "chiens acceptés (intérieur et extérieur)", "LGBTQ+ friendly", "safe place personnes trans",
            "plats bio et végétaliens", "avis clients très contrastés (plusieurs expériences de service décevantes à côté d'avis dithyrambiques) — reflété fidèlement"],
   'services': ["Accessible en fauteuil roulant", "Chiens acceptés", "LGBTQ+ friendly", "Safe place personnes trans", "Plats bio", "Plats végétaliens"],
   'rename': {"cuisine d'inspiration arménienne par le chef-patron Fred, belle sélection de vins nature": "Cuisine d'inspiration arménienne (chef Fred), belle sélection de vins nature",
              "décor deux salles écharpes OM/Arsenal, comptoir orange": "Décor foot OM/Arsenal, comptoir orange"},
 },
 54: {
   'drop': ["artisan", "bakery", "healthy wheat", "natural yeast", "Organic flours", "gluten-free", "With kids"],
   'services': ["Sans gluten (options)", "Adapté aux familles"],
 },
 55: {
   'drop': ["cantine", "traiteur", "produits frais", "plats à emporter", "file d'attente à l'ouverture"],
   'services': ["Traiteur", "Vente à emporter"],
 },
 56: {
   'drop': ["gluten-free", "cookies", "décoration soignée", "accueil chaleureux"],
   'services': ["Sans gluten (options)"],
 },
 57: {
   'drop': ["good deal"],
 },
 58: {
   'drop': ["Breakfast", "gluten-free", "Homemade", "salad", "soup", "tartines", "Take away", "bois et rotin", "coussins colorés"],
   'services': ["Sans gluten (options)", "Vente à emporter"],
   'rename': {"décoration bohème": "Décoration bohème (bois et rotin)"},
 },
 59: {
   'drop': ["terrace", "restaurant", "café", "accessible PMR", "chiens acceptés en terrasse", "LGBTQ+ friendly", "réservations acceptées",
            "plats halal", "plats bio"],
   'services': ["Chiens acceptés", "LGBTQ+ friendly", "Réservations acceptées", "Plats halal", "Plats bio"],
 },
 60: {
   'drop': ["breakfast", "terrasse"],
 },
}

for lieu_id, spec in PLAN.items():
    for t in spec.get('drop', []):
        unlink_tag(lieu_id, t)
    for s in spec.get('services', []):
        add_service(lieu_id, s)
    for old, new in spec.get('rename', {}).items():
        # only rename in context of this lieu's link; since strings are lieu-specific/unique in practice, do a global rename
        rename_tag(old, new)

# cleanup orphan tags (no longer linked to any lieu)
cur.execute("DELETE FROM tags WHERE id NOT IN (SELECT DISTINCT tag_id FROM lieu_tags)")
orphans_removed = cur.rowcount
# cleanup orphan services (shouldn't happen but just in case)
cur.execute("DELETE FROM services WHERE id NOT IN (SELECT DISTINCT service_id FROM lieu_services)")

append_note = ("Nettoyage 'reconnu pour' vs 'service' (14/07/2026) : reclassification des données ajoutées lors de la passe "
               "d'enrichissement Google (lots 8 + généralisation 50 lieux) — les attributs factuels/pratiques (accessibilité, "
               "animaux, réservations, familles, LGBTQ+/trans, options diététiques halal/bio/vegan/sans gluten, happy hour, "
               "vente à emporter, traiteur, télétravail...) déplacés vers 'services' ; les tags trop longs/génériques ou les "
               "nuances d'avis contrastés supprimés de 'reconnu pour' (détail conservé dans source_donnees) ; ne restent en tags "
               "que les éléments réellement distinctifs (spécialités signature, éléments d'ambiance/patrimoine marquants).")
for lieu_id in PLAN:
    append_source(lieu_id, append_note)

con.commit()
print("Tags orphelins supprimés:", orphans_removed)
con.close()
print("OK cleanup")
