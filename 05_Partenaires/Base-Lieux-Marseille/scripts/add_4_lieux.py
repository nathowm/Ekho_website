import sys
sys.path.insert(0, '/tmp/lieux_db')
from lieu_helper import add_lieu, get_lieu_summary

SRC_DATE = "[2026-07-15]"

# ---------------------------------------------------------------------------
# 1) AU COMPTOIR DU LIVRE
# ---------------------------------------------------------------------------
au_comptoir_du_livre = {
    "nom": "Au Comptoir du Livre",
    "lieu_actif": True,
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Cours Julien / La Plaine",
    "adresse": "47 rue des Trois Frères Barthélémy, 13006 Marseille",
    "types": ["Librairie-café"],
    "gamme_prix": "€",
    "cadre": "Mixte",
    "site_web": None,
    "telephone_public": None,
    "horaires": {
        "Lundi": None,
        "Mardi": [("08:30", "21:00")],
        "Mercredi": [("08:30", "21:00")],
        "Jeudi": [("08:30", "21:00")],
        "Vendredi": [("08:30", "21:00")],
        "Samedi": [("08:30", "22:00")],
        "Dimanche": None,
    },
    "phrases_accroche": {
        "Matin": "Un café au calme entouré de livres pour commencer la journée en douceur, gros coussins et coin lecture.",
        "Midi": "Sandwichs faits maison à déguster entre les rayonnages ou en terrasse, café-librairie ouvert en continu.",
        "Après-midi": "L'adresse idéale pour bouquiner un après-midi entier, café à la main, dans une ambiance cocon.",
        "Soir": "Apéro littéraire jusqu'à 21h (22h le samedi) : un verre entre les étagères avant la fermeture.",
    },
    "activites_priorite": {
        "Lire":                 {"Matin": "P", "Midi": "P", "Après-midi": "P", "Soir": "S"},
        "Travailler":           {"Matin": "S", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Jeux de société":      {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Jeux vidéos":          {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Écouter de la musique":{"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Manger":               {"Matin": "-", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Boire un verre":       {"Matin": "-", "Midi": "-", "Après-midi": "S", "Soir": "S"},
        "Boire un café":        {"Matin": "P", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Goûter":               {"Matin": "-", "Midi": "-", "Après-midi": "S", "Soir": "-"},
        "Divertissement":       {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
    },
    "ambiance": {
        "Matin":       {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Midi":        {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable", "Calme"]},
        "Après-midi":  {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Soir":        {"bruit": "Modéré", "luminosite": "Modéré", "musique": "Faible", "affluence": "Faible", "types": ["Sociable"]},
    },
    "services": ["Terrasse", "Livres", "Restauration sur place", "Happy hour"],
    "tags": [
        "Librairie Café",
        "Concept Original",
        "Gros coussins, ambiance cocon lecture",
        "Cours Julien",
    ],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2022/12/Au-comptoir-du-livre_cafe-librairie-Marseille_City-guide_Love-Spots_01.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2022/12/Au-comptoir-du-livre_cafe-librairie-Marseille_City-guide_Love-Spots_35.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2022/12/Au-comptoir-du-livre_cafe-librairie-Marseille_City-guide_Love-Spots_25.jpg",
    ],
    "source_donnees": (
        f"{SRC_DATE} Ajout (demande utilisateur \"Ajoute proprement et finement les lieux suivants\"). "
        "Source unique trouvée : marseille.love-spots.com (14/12/2022), tenu par Nadine et Amalric. Café-librairie "
        "avec gros coussins, terrasse + intérieur, ambiance cocon lecture. Prix : livres dès 3€, café 1,50€, "
        "sandwich 8,50€. Contact : aucomptoirdulivre.librairie@gmail.com (page Facebook uniquement, pas de site "
        "web dédié trouvé, pas de téléphone public trouvé). Horaires Mardi-Vendredi 8h30-21h, Samedi 8h30-22h "
        "explicitement donnés par la source ; fermeture Dimanche et Lundi NON confirmée explicitement, déduite "
        "de l'absence de tag \"open on sundays\" et de la présence du tag \"Open Tuesday evening\" (qui suggère "
        "a contrario que le lundi soir est fermé) — à vérifier/affiner si possible. Aucune fiche Google Maps "
        "synchronisée trouvée sur restaurants-de-france.fr — note_google laissée vide."
    ),
}

# ---------------------------------------------------------------------------
# 2) BEN MOUTURE
# ---------------------------------------------------------------------------
ben_mouture = {
    "nom": "Ben Mouture",
    "lieu_actif": True,
    "code_postal": "13007",
    "arrondissement": "7e",
    "quartier": "Saint-Victor / Corderie",
    "adresse": "34 Rue Petit Chantier, 13007 Marseille",
    "types": ["Café"],
    "gamme_prix": "€",
    "cadre": "Mixte",
    "site_web": "https://www.instagram.com/benmouture/",
    "telephone_public": "06 58 13 87 69",
    "note_google": 4.9,
    "nombre_avis_google": 145,
    "horaires": {
        "Lundi": None,
        "Mardi": [("09:00", "17:00")],
        "Mercredi": [("09:00", "17:00")],
        "Jeudi": [("09:00", "17:00")],
        "Vendredi": [("09:00", "17:00")],
        "Samedi": [("09:00", "17:00")],
        "Dimanche": None,
    },
    "phrases_accroche": {
        "Matin": "Torréfaction artisanale et grand choix de thés : un café d'exception pour démarrer la journée à Saint-Victor.",
        "Midi": "V60, cappuccino ou jus frais à emporter ou sur la petite terrasse, entre deux visites du quartier.",
        "Après-midi": "Une pause café accueillie par un excellent espresso et une sélection de thés soignée, adaptée au travail sur ordinateur.",
        "Soir": None,
    },
    "activites_priorite": {
        "Lire":                 {"Matin": "S", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Travailler":           {"Matin": "P", "Midi": "P", "Après-midi": "P", "Soir": "-"},
        "Jeux de société":      {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Jeux vidéos":          {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Écouter de la musique":{"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Manger":               {"Matin": "S", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Boire un verre":       {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Boire un café":        {"Matin": "P", "Midi": "P", "Après-midi": "P", "Soir": "-"},
        "Goûter":               {"Matin": "-", "Midi": "-", "Après-midi": "S", "Soir": "-"},
        "Divertissement":       {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
    },
    "ambiance": {
        "Matin":       {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Midi":        {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable", "Dynamique"]},
        "Après-midi":  {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme", "Sociable"]},
        "Soir":        {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
    },
    "services": [
        "Terrasse", "Vente à emporter", "Livraison", "Accessible en fauteuil roulant",
        "Adapté aux familles", "Adapté au travail sur ordinateur", "Toilettes",
        "Restauration sur place",
    ],
    "tags": ["Excellent café", "Grand choix de thés"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2023/09/Ben-Mouture_Marseille_City-Guide_Love-Spots_02.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2023/09/Ben-Mouture_Marseille_City-Guide_Love-Spots_01.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2023/09/Ben-Mouture_Marseille_City-Guide_Love-Spots_03.jpg",
    ],
    "source_donnees": (
        f"{SRC_DATE} Ajout (demande utilisateur \"Ajoute proprement et finement les lieux suivants\"). "
        "VÉRIFIÉ via fetch direct de https://cafe.restaurants-de-france.fr/ben-mouture-3921845.html "
        "(fiche synchronisée Google Maps, mention explicite de synchronisation, dernière mise à jour 09/12/2025) : "
        "note 4,9/5 sur 145 avis. Bloc \"à propos\" Google (-> services, Règle 14.7) : ambiance décontractée/"
        "branché, clientèle étudiants/touristes, chaises hautes/convient aux enfants, paiements CB/débit/NFC, "
        "populaire pour travail sur ordinateur portable (-> Travailler noté P, sourcé), toilettes, petit-déj/"
        "desserts/places assises/brunch, terrasse/drive/vente à emporter/repas sur place/livraison. Points forts "
        "Google (-> tags) : \"Excellent café\", \"Grand choix de thés\". HORAIRES : divergence entre deux sources non "
        "résolue avec certitude — love-spots.com (22/09/2023, source primaire datée et détaillée) indique "
        "\"Mardi > Samedi de 9h à 17h\" (fermé dimanche-lundi) ; une autre agrégation WebSearch non datée indique "
        "\"Lundi-Vendredi 9h-17h, Samedi 9h-13h, fermé dimanche\". Retenu ici : la version love-spots (source "
        "primaire nommée, datée, avec journaliste identifiée), par cohérence avec la préférence du projet pour "
        "les sources primaires détaillées sur les agrégats non datés — à confirmer si possible. Prix (love-spots) : "
        "Espresso 2€, Cappuccino 3,50€, V60 5€, Matcha Latte 4€, Jus frais 4€. Aucun site web officiel dédié "
        "trouvé, Instagram @benmouture utilisé comme site_web par défaut."
    ),
}

# ---------------------------------------------------------------------------
# 3) LA TISSERIE
# ---------------------------------------------------------------------------
la_tisserie = {
    "nom": "La Tisserie",
    "lieu_actif": True,
    "code_postal": "13007",
    "arrondissement": "7e",
    "quartier": "Saint-Victor / Endoume",
    "adresse": "142 Rue d'Endoume, 13007 Marseille",
    "types": ["Café"],
    "gamme_prix": "€",
    "cadre": "Intérieur",
    "site_web": "https://www.tisserie.coffee",
    "telephone_public": "04 91 89 22 69",
    "horaires": {
        "Lundi": None,
        "Mardi": [("10:00", "19:00")],
        "Mercredi": [("10:00", "19:00")],
        "Jeudi": [("10:00", "19:00")],
        "Vendredi": [("10:00", "19:00")],
        "Samedi": [("09:00", "13:00")],
        "Dimanche": [("09:00", "13:00")],
    },
    "phrases_accroche": {
        "Matin": "Torréfaction artisanale et espresso soigné, entre Saint-Victor et Endoume : le café de quartier version spécialité.",
        "Midi": "Une pause café accompagnée des viennoiseries voisines (Maison Saint-Honoré) ou d'un cookie d'Encore Un Morceau.",
        "Après-midi": "Grains en vente au comptoir (9 à 21€ le sachet), conseillés par Gallien, torréfacteur formé à l'Atelier de Torréfaction à Paris.",
        "Soir": None,
    },
    "activites_priorite": {
        "Lire":                 {"Matin": "S", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Travailler":           {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Jeux de société":      {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Jeux vidéos":          {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Écouter de la musique":{"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Manger":               {"Matin": "S", "Midi": "S", "Après-midi": "-", "Soir": "-"},
        "Boire un verre":       {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Boire un café":        {"Matin": "P", "Midi": "P", "Après-midi": "P", "Soir": "-"},
        "Goûter":               {"Matin": "-", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Divertissement":       {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
    },
    "ambiance": {
        "Matin":       {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Midi":        {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi":  {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Soir":        {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
    },
    "services": ["Boutique", "Vente à emporter"],
    "tags": [
        "Torréfaction Artisanale",
        "Grains en vente (9-21€/sachet), conseils personnalisés du torréfacteur",
        "Cookies et viennoiseries de commerçants voisins (Encore Un Morceau, Maison Saint-Honoré)",
    ],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Tisserie_Torrefaction_Marseille_City-Guide_Love-Spots_01.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Tisserie_Torrefaction_Marseille_City-Guide_Love-Spots_10-1.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Tisserie_Torrefaction_Marseille_City-Guide_Love-Spots_08-2.jpg",
    ],
    "source_donnees": (
        f"{SRC_DATE} Ajout (demande utilisateur \"Ajoute proprement et finement les lieux suivants\"). "
        "Source primaire : fetch direct de marseille.love-spots.com/en/spots/eating-out/cafe-en/135630-la-tisserie.html "
        "(article du 24/12/2021, màj 29/12/2021), qui donne explicitement \"Tuesday > Friday from 10:00 to 19:00 / "
        "Saturday and Sunday from 9:00 to 13:00\" (fermé lundi) — retenu ici. Une agrégation WebSearch distincte "
        "évoquait une coupure méridienne (\"10h-13h30 / 15h-19h\") non confirmée par la source primaire directe — "
        "non retenue en cas de conflit, mais à vérifier sur place si possible. Fermeture à 19h : le créneau "
        "\"Soir\" (18h30-3h) n'est donc pratiquement jamais couvert (au plus 30 min sur 4 jours) — traité comme "
        "\"Non applicable\" par cohérence avec le traitement des lieux fermés le soir ailleurs dans le projet. "
        "Propriétaire : Gallien Jeanroy, ex-éducateur spécialisé, torréfacteur depuis ~2021 (ouverture sept. 2021, "
        "local ex-poissonnerie puis salon de coiffure), formé lors d'un séjour en Australie (2014) puis à "
        "l'Atelier de Torréfaction (Bastille, Paris) — sources le-grand-pastis.com (10/03/2022, màj 15/05/2025) "
        "et timeout.fr (17/04/2025). Prix : espresso 2€ (double 3€), cappuccino 3,50€ (lait d'avoine sans "
        "supplément), matcha 5€, grains 9-21€/sachet, quart de café 7,50-12€. Produits voisins revendus : "
        "cookies \"Encore Un Morceau\" (3,50€), viennoiseries \"Maison Saint-Honoré\" (week-ends uniquement). "
        "Notes trouvées mais explicitement NON-Google (Restaurant Guru 4,9/156 avis ; Sluurpy 5,0/90 avis ; "
        "Timeout 5/5 = note éditoriale) — non reportées en note_google, conformément à la règle vérifié/agrégé. "
        "Aucune fiche Google Maps synchronisée trouvée sur restaurants-de-france.fr — note_google laissée vide."
    ),
}

# ---------------------------------------------------------------------------
# 4) MAISON DES NINES  (corrigé depuis "Maison des Nimes", mishearing/coquille)
# ---------------------------------------------------------------------------
maison_des_nines = {
    "nom": "Maison des Nines",
    "lieu_actif": True,
    "code_postal": "13001",
    "arrondissement": "1er",
    "quartier": "Noailles",
    "adresse": "9 rue d'Aubagne, 13001 Marseille",
    "types": ["Café", "Restaurant"],
    "gamme_prix": "€",
    "cadre": "Mixte",
    "site_web": "https://www.instagram.com/maisondesnines/",
    "telephone_public": "06 65 54 32 30",
    "horaires": {
        "Lundi": None,
        "Mardi": [("09:30", "19:00")],
        "Mercredi": [("09:30", "19:00")],
        "Jeudi": [("09:30", "19:00")],
        "Vendredi": [("09:30", "19:00")],
        "Samedi": [("09:30", "19:00")],
        "Dimanche": [("11:00", "16:00")],
    },
    "phrases_accroche": {
        "Matin": "Café-cantine et boutique éco-responsable à Noailles : petit-déjeuner et premiers achats déco/mode dès 9h30.",
        "Midi": "Cuisine méditerranéenne de saison, labellisée 2 Ecotables, à déguster en tables d'hôtes au cœur des 4 \"univers\" de la maison.",
        "Après-midi": "Entre brunch tardif et ateliers créatifs, la Maison des Nines se vit comme un lieu de vie autant qu'un restaurant.",
        "Soir": None,
    },
    "activites_priorite": {
        "Lire":                 {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Travailler":           {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Jeux de société":      {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Jeux vidéos":          {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Écouter de la musique":{"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Manger":               {"Matin": "S", "Midi": "P", "Après-midi": "S", "Soir": "-"},
        "Boire un verre":       {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Boire un café":        {"Matin": "P", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Goûter":               {"Matin": "-", "Midi": "-", "Après-midi": "S", "Soir": "-"},
        "Divertissement":       {"Matin": "-", "Midi": "-", "Après-midi": "S", "Soir": "-"},
    },
    "ambiance": {
        "Matin":       {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Midi":        {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi":  {"bruit": "Modéré", "luminosite": "Modéré", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir":        {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
    },
    "services": ["Boutique", "Boutique engagée", "Ateliers créatifs", "Terrasse", "Adapté aux familles"],
    "tags": [
        "Concept Store",
        "Café-Canteen",
        "Table d'hôtes",
        "Labellisé 2 Ecotables",
        "4 univers thématiques (cuisine, salle de bain, dressing, salle à manger)",
        "Noailles",
    ],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2021/07/Maison-des-Nines_Boutique-Cantine_Table-d-hote_Noailles_Marseille_City-Guide_Love-Spots_11.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2021/07/Maison-des-Nines_Boutique-Cantine_Table-d-hote_Noailles_Marseille_City-Guide_Love-Spots_04.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2021/07/Maison-des-Nines_Boutique-Cantine_Table-d-hote_Noailles_Marseille_City-Guide_Love-Spots_05.jpg",
    ],
    "source_donnees": (
        f"{SRC_DATE} Ajout (demande utilisateur \"Ajoute proprement et finement les lieux suivants ... / Maison des "
        "nimes\"). CORRECTION DE NOM : \"Maison des nimes\" est une coquille/mécoute pour le nom réel de "
        "l'établissement, \"Maison des Nines\" (aussi stylisé \"La Maison des Nines\"), à Noailles — confirmé par "
        "recherche croisée (aucun établissement \"Maison des Nîmes\" trouvé à Marseille, alors que \"Maison des "
        "Nines\" correspond exactement à l'adresse et au concept décrits). Source principale : marseille.love-"
        "spots.com (05/07/2021). Concept : café-cantine + boutique (mode/beauté/déco éco-responsable) + tables "
        "d'hôtes + ateliers créatifs, fondé par 3 jeunes femmes (Annaëlle, Estelle et Claire selon une source "
        "secondaire BGE), ouvert en 2021 post-covid. 4 pièces = 4 \"univers\" (cuisine, salle de bain, dressing, "
        "salle à manger). Labellisé 2 Ecotables (cuisine méditerranéenne/de saison). Prix : café 1,50€, entrées "
        "5-8€, plats 12,50-14,50€, dessert 3,50-5€, vin 3,50€, menu à emporter 11,50€. Contact : "
        "contact@maisondesnines.com, Facebook (facebook.com/Maison-des-Nines-108703964288322), Instagram "
        "@maisondesnines (utilisé comme site_web par défaut, aucun site officiel dédié trouvé). Fermeture à 19h "
        "(16h le dimanche) : créneau \"Soir\" traité comme \"Non applicable\", par cohérence avec le traitement "
        "des lieux fermés le soir ailleurs dans le projet. Avis TripAdvisor mitigés mentionnés dans une source "
        "secondaire mais aucune note chiffrée fiable extraite — non reportés. Aucune fiche Google Maps "
        "synchronisée trouvée sur restaurants-de-france.fr — note_google laissée vide."
    ),
}

# ---------------------------------------------------------------------------
lieux_a_ajouter = [
    ("Au Comptoir du Livre", au_comptoir_du_livre),
    ("Ben Mouture", ben_mouture),
    ("La Tisserie", la_tisserie),
    ("Maison des Nines", maison_des_nines),
]

ids = {}
for nom, data in lieux_a_ajouter:
    new_id = add_lieu(data)
    ids[nom] = new_id
    print(f"-> {nom} inséré avec id={new_id}")

print()
print("Vérification rapide :")
for nom, lid in ids.items():
    s = get_lieu_summary(lid)
    print(f"  [{lid}] {s['nom']} | types={s['types']} | adresse={s['adresse']} | "
          f"tel={s['telephone_public']} | services={len(s['services'])} | tags={len(s['tags'])}")
