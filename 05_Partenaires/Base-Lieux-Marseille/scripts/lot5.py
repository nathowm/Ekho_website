# -*- coding: utf-8 -*-
from lieu_helper import add_lieu

lieux = []

# ---------- Maurice ----------
lieux.append({
    "nom": "Maurice",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Café", "Bar", "Restaurant"],
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Notre Dame du Mont / Lodi",
    "adresse": "76 Rue de Lodi, 13006 Marseille",
    "latitude": 43.2908,
    "longitude": 5.3899,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": None,
    "telephone_public": "09 56 45 36 75",
    "niveau_engagement": None,
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (18/04/2025), Instagram @maurice.marseille "
        "(seul lien officiel trouvé, pas de site web dédié identifié). Café-bar-restaurant de quartier "
        "rue de Lodi, entre petit-déjeuner, carte bistrotière et sélection de vins natures/traditionnels."
    ),
    "horaires": {
        "Lundi": None,
        "Mardi": [("08:30", "23:59")],
        "Mercredi": [("08:30", "23:59")],
        "Jeudi": [("08:30", "23:59")],
        "Vendredi": [("08:30", "23:59")],
        "Samedi": [("08:30", "23:59")],
        "Dimanche": None,
    },
    "phrases_accroche": {
        "Matin": "Petit-déjeuner et premiers cafés sur la terrasse ensoleillée de la rue de Lodi.",
        "Midi": "Menu du midi entrée-plat-dessert et carte bistrotière généreuse.",
        "Après-midi": "Une pause tranquille autour d'un verre de vin nature, sur le pouce ou en salle.",
        "Soir": "Ambiance conviviale jusqu'à minuit, entre bons petits plats et jolies quilles.",
    },
    "contact": None,
    "activites_priorite": {
        "Boire un café": {"Matin": "P", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Manger": {"Matin": "S", "Midi": "P", "Après-midi": "-", "Soir": "P"},
        "Boire un verre": {"Matin": "-", "Midi": "S", "Après-midi": "S", "Soir": "P"},
    },
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme", "Sociable"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Modéré", "luminosite": "Faible", "musique": "Modéré", "affluence": "Fort", "types": ["Sociable"]},
    },
    "services": ["Terrasse"],
    "tags": ["Bistrot de Quartier", "Brunch", "Vins Nature", "Terrasse Ensoleillée", "Avec Enfants"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2025/04/Maurice_bistrot-bar-cantine_Marseille_Love-spots_09.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/04/Maurice_bistrot-bar-cantine_Marseille_Love-spots_07.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/04/Maurice_bistrot-bar-cantine_Marseille_Love-spots_16.jpeg",
    ],
})

# ---------- Les Babines de Mars ----------
lieux.append({
    "nom": "Les Babines de Mars",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Restaurant", "Bistrot"],
    "code_postal": "13001",
    "arrondissement": "1er",
    "quartier": "Longchamp",
    "adresse": "135 rue Consolat (angle rue Louis Grobet), 13001 Marseille",
    "latitude": 43.3080,
    "longitude": 5.3919,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": None,
    "telephone_public": "04 91 07 61 36",
    "niveau_engagement": None,
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (30/05/2025), Instagram @lesbabinesdemars.restaurant "
        "(seul lien officiel trouvé). Restaurant bistronomique du quartier Longchamp, ayant repris "
        "l'esprit bistrot de l'ancien 'Les Eaux de Mars' avec une touche plus créative."
    ),
    "horaires": {
        "Lundi": [("11:00", "14:00"), ("19:00", "23:30")],
        "Mardi": [("11:00", "14:00"), ("19:00", "23:30")],
        "Mercredi": [("11:00", "14:00"), ("19:00", "23:30")],
        "Jeudi": [("11:00", "14:00"), ("19:00", "23:30")],
        "Vendredi": [("11:00", "14:00"), ("19:00", "23:30")],
        "Samedi": None,
        "Dimanche": None,
    },
    "phrases_accroche": {
        "Matin": None,
        "Midi": "Formule midi soignée et créative, héritage bistrot assumé.",
        "Après-midi": None,
        "Soir": "Assiettes à partager pensées pour la convivialité, accompagnées d'un joli verre de vin nature.",
    },
    "contact": None,
    "activites_priorite": {
        "Manger": {"Matin": "-", "Midi": "P", "Après-midi": "-", "Soir": "P"},
        "Boire un verre": {"Matin": "-", "Midi": "S", "Après-midi": "-", "Soir": "S"},
    },
    "ambiance": {
        "Matin": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
        "Soir": {"bruit": "Modéré", "luminosite": "Modéré", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
    },
    "services": ["Terrasse"],
    "tags": ["Bistronomie", "Vins Nature", "Longchamp", "Plats à Partager", "Terrasse"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2025/05/Les-Babines-de-Mars_Bistrot-Marseille_Love-spots_12.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/05/Les-Babines-de-Mars_Bistrot-Marseille_Love-spots_13.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/05/Les-Babines-de-Mars_Bistrot-Marseille_Love-spots_07.jpeg",
    ],
})

# ---------- Yuzu Record Bar ----------
lieux.append({
    "nom": "Yuzu Record Bar",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Restaurant", "Bar"],
    "code_postal": "13001",
    "arrondissement": "1er",
    "quartier": "Noailles",
    "adresse": "36 rue d'Aubagne, 13001 Marseille",
    "latitude": 43.2971,
    "longitude": 5.3773,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": "http://www.yuzu-record-bar.com/",
    "telephone_public": "09 50 15 78 16",
    "niveau_engagement": None,
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (09/01/2026). Adresse historique du quartier Noailles ; "
        "concept hybride restaurant / bar audiophile (système Hi-Fi haut de gamme, programmation DJ) / galerie "
        "d'art avec expositions tournantes."
    ),
    "horaires": {
        "Lundi": None,
        "Mardi": None,
        "Mercredi": [("18:00", "23:59")],
        "Jeudi": None,
        "Vendredi": [("17:00", "02:00")],
        "Samedi": [("17:00", "02:00")],
        "Dimanche": [("17:00", "02:00")],
    },
    "phrases_accroche": {
        "Matin": None,
        "Midi": None,
        "Après-midi": "Ouverture en douceur dès 17h le week-end, entre platines et premiers verres.",
        "Soir": "Système son audiophile, DJ et tapas méditerranéennes jusque tard dans la nuit.",
    },
    "contact": None,
    "activites_priorite": {
        "Boire un verre": {"Matin": "-", "Midi": "-", "Après-midi": "S", "Soir": "P"},
        "Manger": {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "S"},
        "Écouter de la musique": {"Matin": "-", "Midi": "-", "Après-midi": "O", "Soir": "F"},
    },
    "ambiance": {
        "Matin": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
        "Midi": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Modéré", "musique": "Modéré", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Fort", "luminosite": "Faible", "musique": "Fort", "affluence": "Fort", "types": ["Dynamique", "Sociable"]},
    },
    "services": ["Terrasse"],
    "tags": ["Bar Audiophile", "DJ", "Galerie d'Art", "Hi-Fi Bar", "Noailles", "Tapas Méditerranéennes"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2025/12/Yuzu-record-bar_Bar-audiophile_Marseille_Love-Spots_10.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/12/Yuzu-record-bar_Bar-audiophile_Marseille_Love-Spots_13.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/12/Yuzu-record-bar_Bar-audiophile_Marseille_Love-Spots_05.jpeg",
    ],
})

# ---------- Grand Écart ----------
lieux.append({
    "nom": "Grand Écart",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Café", "Bar"],
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Notre Dame du Mont / Lodi",
    "adresse": "18 Rue Fontange, 13006 Marseille",
    "latitude": 43.2934,
    "longitude": 5.3862,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": "http://www.grandecart.com",
    "telephone_public": "04 91 42 39 90",
    "niveau_engagement": None,
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (24/12/2025, l'article ne précise pas l'adresse exacte) "
        "croisé avec Pagesjaunes.fr et Privateaser.com pour confirmer l'adresse (18 Rue Fontange, 13006), "
        "site officiel grandecart.com, Instagram @grandecart.marseille. Concept hybride 'Social Sport Club' : "
        "salle de sport (boxe, bootcamp), cantine locavore et bar à vins nature réunis dans un même lieu, "
        "quartier Notre-Dame-du-Mont. Dimanche fermé (non mentionné dans les horaires publiés)."
    ),
    "horaires": {
        "Lundi": [("07:45", "20:00")],
        "Mardi": [("07:45", "20:00")],
        "Mercredi": [("07:45", "20:00")],
        "Jeudi": [("07:45", "22:00")],
        "Vendredi": [("07:45", "22:00")],
        "Samedi": [("09:00", "22:00")],
        "Dimanche": None,
    },
    "phrases_accroche": {
        "Matin": "Café de spécialité et premiers exercices pour bien démarrer la journée.",
        "Midi": "Cantine locavore et plats du jour entre deux séances de sport.",
        "Après-midi": "Un espace hybride pour enchaîner burpees et pause gourmande.",
        "Soir": "Un verre de vin nature (avec modération) pour clore une séance de boxe ou de bootcamp.",
    },
    "contact": None,
    "activites_priorite": {
        "Boire un café": {"Matin": "P", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Manger": {"Matin": "-", "Midi": "P", "Après-midi": "-", "Soir": "-"},
        "Boire un verre": {"Matin": "-", "Midi": "-", "Après-midi": "S", "Soir": "S"},
    },
    "ambiance": {
        "Matin": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Modéré", "affluence": "Modéré", "types": ["Dynamique"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Soir": {"bruit": "Modéré", "luminosite": "Modéré", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
    },
    "services": ["Wifi"],
    "tags": ["Social Sport Club", "Salle de Sport", "Cantine Locavore", "Bar à Vins Nature", "Boxe", "Notre-Dame-du-Mont"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2025/12/Grand-ecart_Social-sport-club_marseille_Love-spots_04.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/12/Grand-ecart_Social-sport-club_marseille_Love-spots_05.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/12/Grand-ecart_Social-sport-club_marseille_Love-spots_11.jpeg",
    ],
})

# ---------- 7VB Café ----------
lieux.append({
    "nom": "7VB Café",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Café"],
    "code_postal": "13002",
    "arrondissement": "2e",
    "quartier": "Panier",
    "adresse": "9 Rue Caisserie, 13002 Marseille",
    "latitude": 43.2977,
    "longitude": 5.3702,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": "http://www.7vbcafe.fr",
    "telephone_public": None,
    "niveau_engagement": None,
    "gamme_prix": "€",
    "cadre": "Intérieur",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (09/11/2018, source ancienne à reconfirmer sur place). "
        "Coffee shop associatif du Panier, propose cafés de qualité, pâtisseries maison et un espace dédié "
        "aux enfants ; également identifié comme bon lieu pour travailler. Aucun téléphone public trouvé."
    ),
    "horaires": {
        "Lundi": [("10:30", "19:00")],
        "Mardi": [("10:30", "19:00")],
        "Mercredi": None,
        "Jeudi": [("10:30", "19:00")],
        "Vendredi": [("10:30", "19:00")],
        "Samedi": [("10:30", "19:00")],
        "Dimanche": [("13:00", "17:00")],
    },
    "phrases_accroche": {
        "Matin": "Cafés de qualité et douceurs maison dans une ambiance associative et chaleureuse.",
        "Midi": "Une pause légère entre sandwich et bon café, avec un coin dédié aux enfants.",
        "Après-midi": "Le goûter parfait : pâtisserie maison et café soigné, au calme ou en travaillant.",
        "Soir": None,
    },
    "contact": None,
    "activites_priorite": {
        "Boire un café": {"Matin": "P", "Midi": "S", "Après-midi": "P", "Soir": "-"},
        "Travailler": {"Matin": "S", "Midi": "-", "Après-midi": "S", "Soir": "-"},
        "Goûter": {"Matin": "-", "Midi": "-", "Après-midi": "P", "Soir": "-"},
    },
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Modéré", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
    },
    "services": ["Wifi", "Espace Enfants"],
    "tags": ["Café Associatif", "Espace Enfants", "Fait Maison", "Le Panier", "Coin Travail"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop_Marseille_7VB_Love-spots_01.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop_Marseille_7VB_Love-spots_02.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop_Marseille_7VB_Love-spots_11.jpg",
    ],
})

ids = []
for data in lieux:
    lid = add_lieu(data)
    ids.append((lid, data["nom"]))
    print("Inséré :", lid, data["nom"])

print(ids)
