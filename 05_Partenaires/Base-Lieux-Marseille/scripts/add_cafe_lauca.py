import sys
sys.path.insert(0, '/tmp/lieux_db')
from lieu_helper import add_lieu, get_lieu_summary

SRC_DATE = "[2026-07-15]"

cafe_lauca = {
    "nom": "Café Lauca « La Boutchica »",
    "lieu_actif": True,
    "code_postal": "13001",
    "arrondissement": "1er",
    "quartier": "Palais de Justice / Cours d'Estienne d'Orves",
    "adresse": "68 rue Grignan, 13001 Marseille",
    "types": ["Café"],
    "gamme_prix": "€",
    "cadre": "Mixte",
    "site_web": "https://www.cafelauca.com/cafe-lauca-cafe-de-specialite-a-marseille",
    "telephone_public": "07 67 30 86 37",
    "horaires": {
        "Lundi":    [("07:00", "19:00")],
        "Mardi":    [("07:00", "19:00")],
        "Mercredi": [("07:00", "19:00")],
        "Jeudi":    [("07:00", "19:00")],
        "Vendredi": [("07:00", "19:00")],
        "Samedi":   [("08:00", "19:00")],
        "Dimanche": [("08:00", "17:00")],
    },
    "phrases_accroche": {
        "Matin": "Le plus petit coffee shop de Marseille (12 m²) : cafés de spécialité torréfiés à Aubagne, en grain ou moulu, dès 7h.",
        "Midi": "Une pause espresso ou boisson lactée, conseillée par l'équipe, entre Palais de Justice et Cours d'Estienne d'Orves.",
        "Après-midi": "Grains à emporter et sélection de thés L'Infusion Marseille, dans un cadre minuscule mais chaleureux.",
        "Soir": None,
    },
    "activites_priorite": {
        "Lire":                 {"Matin": "S", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Travailler":           {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
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
        "Matin":       {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable", "Dynamique"]},
        "Midi":        {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable", "Dynamique"]},
        "Après-midi":  {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Modéré", "types": ["Calme", "Sociable"]},
        "Soir":        {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
    },
    "services": ["Vente à emporter", "Boutique", "Terrasse"],
    "tags": [
        "Torréfaction Artisanale",
        "Plus petit coffee shop de Marseille (12 m²)",
        "Café colombien, torréfié à Aubagne (histoire de Laurent)",
        "Cours d'Estienne d'Orves",
    ],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2021/11/Cafe-Lauca_La-Boutchica-_coffee-shop_marseille_City-guide_Love-Spots_09.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2021/11/Cafe-Lauca_La-Boutchica-_coffee-shop_marseille_City-guide_Love-Spots_06.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2021/11/Cafe-Lauca_La-Boutchica-_coffee-shop_marseille_City-guide_Love-Spots_02.jpg",
    ],
    "source_donnees": (
        f"{SRC_DATE} Ajout (demande utilisateur \"ajout Café Lauca 'la Boutchika'\"). CORRECTION D'ORTHOGRAPHE : "
        "le nom officiel du coffee shop est \"La Boutchica\" (et non \"la Boutchika\" comme orthographié dans la "
        "demande) — confirmé par le site officiel cafelauca.com et par marseille.love-spots.com. Deux sources "
        "croisées : (1) fetch direct de marseille.love-spots.com/en/spots/eating-out/cafe-en/134711-cafe-lauca-"
        "la-boutchica.html (12/11/2021, par Julie Desbiolles) : \"12m² corridor\", espresso 1,80€, cafés en grain "
        "entre 7,50€ et 9,50€, tél 07 67 30 86 37, lien Instagram @cafe_lauca ; (2) fetch direct de la page "
        "officielle cafelauca.com/cafe-lauca-cafe-de-specialite-a-marseille : confirme l'adresse et le "
        "téléphone, donne l'histoire du fondateur Laurent (origine colombienne, torréfaction artisanale à "
        "Aubagne depuis début 2021, café équitable), la sélection de thés L'Infusion Marseille, contact "
        "contact@cafelauca.fr, ligne directe fondateur 06 38 83 60 40. HORAIRES : la source officielle "
        "(cafelauca.com, la plus récente) donne \"Lundi-Vendredi 7h-19h, Samedi 8h-19h, Dimanche 8h-17h\" — "
        "retenue ici en priorité sur l'article love-spots de 2021 (\"tous les jours ou presque de 7h à 16h\", "
        "horaires visiblement obsolètes vu l'écart important). Une agrégation WebSearch tierce (pagesjaunes) "
        "donne des horaires très proches mais légèrement différents (samedi 8h-18h45, dimanche 8h-17h) — écart "
        "mineur non résolu, site officiel retenu comme référence. Fermeture à 19h (17h dimanche) : créneau "
        "\"Soir\" traité comme \"Non applicable\" par cohérence avec le traitement des lieux fermés le soir "
        "ailleurs dans le projet, malgré un léger débordement théorique 18h30-19h. Aucune fiche Google Maps "
        "synchronisée trouvée sur restaurants-de-france.fr — note_google laissée vide. Espace très réduit "
        "(12 m², \"corridor\") : probablement service debout/comptoir plutôt que assis — activité \"Travailler\" "
        "non cochée en conséquence."
    ),
}

new_id = add_lieu(cafe_lauca)
print(f"-> Café Lauca « La Boutchica » inséré avec id={new_id}")
s = get_lieu_summary(new_id)
print(f"  [{new_id}] {s['nom']} | types={s['types']} | adresse={s['adresse']} | tel={s['telephone_public']} | "
      f"services={s['services']} | tags={s['tags']}")
