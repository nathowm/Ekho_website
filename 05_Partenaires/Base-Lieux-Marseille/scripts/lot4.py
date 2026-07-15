# -*- coding: utf-8 -*-
from lieu_helper import add_lieu

lieux = []

# ---------- Mon Gâté ----------
lieux.append({
    "nom": "Mon Gâté",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Café"],
    "code_postal": "13001",
    "arrondissement": "1er",
    "quartier": "Opéra",
    "adresse": "8 rue du Jeune Anacharsis, 13001 Marseille",
    "latitude": 43.2947,
    "longitude": 5.3773,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": None,
    "telephone_public": "04 86 68 31 63",
    "niveau_engagement": None,
    "gamme_prix": "€",
    "cadre": "Intérieur",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (18/03/2024), Instagram @mongate_marseille. "
        "Premier café à Marseille où choux et profiteroles sont préparés et garnis à la demande "
        "sous les yeux du client."
    ),
    "horaires": {
        "Lundi": None,
        "Mardi": None,
        "Mercredi": [("10:30", "19:00")],
        "Jeudi": [("10:30", "19:00")],
        "Vendredi": [("10:30", "19:00")],
        "Samedi": [("10:30", "19:00")],
        "Dimanche": [("10:30", "17:00")],
    },
    "phrases_accroche": {
        "Matin": "Un chou fraîchement garni pour accompagner le café du matin.",
        "Midi": "Une pause gourmande entre deux rendez-vous : chou classique ou profiterole glacée.",
        "Après-midi": "Le goûter signature : choux à la crème préparés à la demande sous vos yeux.",
        "Soir": "Une dernière douceur sucrée avant la fermeture, pour finir la journée en beauté.",
    },
    "contact": None,
    "activites_priorite": {
        "Goûter": {"Matin": "S", "Midi": "P", "Après-midi": "P", "Soir": "S"},
        "Boire un café": {"Matin": "P", "Midi": "S", "Après-midi": "S", "Soir": "-"},
    },
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Soir": {"bruit": "Faible", "luminosite": "Faible", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
    },
    "services": ["Terrasse"],
    "tags": ["Choux à la Crème", "Profiteroles", "Pâtisserie sur Place", "Fait Devant Vous", "Gourmand"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2024/03/Mon-Gate_Cafe_Choux_Marseille_Love-spots_01.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2024/03/Mon-Gate_Cafe_Choux_Marseille_Love-spots_03.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2024/03/Mon-Gate_Cafe_Choux_Marseille_Love-spots_11.jpeg",
    ],
})

# ---------- Josie ----------
lieux.append({
    "nom": "Josie",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Café"],
    "code_postal": "13005",
    "arrondissement": "5e",
    "quartier": "Chave / Camas",
    "adresse": "56 rue de Bruys, 13005 Marseille",
    "latitude": 43.2938,
    "longitude": 5.3960,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": None,
    "telephone_public": None,
    "niveau_engagement": None,
    "gamme_prix": "€€",
    "cadre": "Intérieur",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (03/11/2025), Instagram @josiecafe.marseille. "
        "Café de spécialité tenu par les sœurs Josse ; contact via hello@josiecoffee.fr "
        "(pas de téléphone public trouvé)."
    ),
    "horaires": {
        "Lundi": [("08:30", "18:00")],
        "Mardi": [("08:30", "18:00")],
        "Mercredi": [("08:30", "18:00")],
        "Jeudi": [("08:30", "18:00")],
        "Vendredi": [("08:30", "18:00")],
        "Samedi": None,
        "Dimanche": None,
    },
    "phrases_accroche": {
        "Matin": "Café de spécialité et petit-déjeuner ensoleillé façon maison provençale.",
        "Midi": "Une formule légère entre deux ateliers, œuf coque et jus maison au menu.",
        "Après-midi": "Un goûter gourmand à savourer dans une ambiance lumineuse et conviviale.",
        "Soir": None,
    },
    "contact": None,
    "activites_priorite": {
        "Boire un café": {"Matin": "P", "Midi": "S", "Après-midi": "P", "Soir": "-"},
        "Goûter": {"Matin": "S", "Midi": "S", "Après-midi": "P", "Soir": "-"},
        "Travailler": {"Matin": "S", "Midi": "-", "Après-midi": "S", "Soir": "-"},
    },
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
    },
    "services": ["Wifi"],
    "tags": ["Café de Spécialité", "Ateliers Créatifs", "Provençal", "Lumineux", "Convivial"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2025/10/Josie_coffee-shop_Marseille_Love-Spots_15.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/10/Josie_coffee-shop_Marseille_Love-Spots_05.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/10/Josie_coffee-shop_Marseille_Love-Spots_16.jpeg",
    ],
})

# ---------- Brûlerie Möka ----------
lieux.append({
    "nom": "Brûlerie Möka",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Café"],
    "code_postal": "13005",
    "arrondissement": "5e",
    "quartier": "Chave / Camas",
    "adresse": "36 Boulevard Eugène Pierre, 13005 Marseille",
    "latitude": 43.2965,
    "longitude": 5.3958,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": "http://brulerie-moka.com/",
    "telephone_public": "06 16 52 14 88",
    "niveau_engagement": None,
    "gamme_prix": "€",
    "cadre": "Mixte",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (05/10/2019, source ancienne à reconfirmer). "
        "Café-torréfacteur artisanal. NB : la source mentionne des horaires \"8h30-18h, sauf 15h\" "
        "sans préciser la nature de cette coupure (pause déjeuner ? jour particulier ?) - "
        "à clarifier sur place ou via le site brulerie-moka.com."
    ),
    "horaires": {
        "Lundi": None,
        "Mardi": [("08:30", "18:00")],
        "Mercredi": [("08:30", "18:00")],
        "Jeudi": [("08:30", "18:00")],
        "Vendredi": [("08:30", "18:00")],
        "Samedi": [("08:30", "18:00")],
        "Dimanche": None,
    },
    "phrases_accroche": {
        "Matin": "Café fraîchement torréfié à savourer dans la salle bistrot ou sous l'arbre.",
        "Midi": "Petite restauration légère autour d'un espresso de torréfaction artisanale.",
        "Après-midi": "Pâtisserie maison et café de spécialité, en salle ou en terrasse ombragée.",
        "Soir": None,
    },
    "contact": None,
    "activites_priorite": {
        "Boire un café": {"Matin": "P", "Midi": "S", "Après-midi": "P", "Soir": "-"},
        "Manger": {"Matin": "-", "Midi": "S", "Après-midi": "-", "Soir": "-"},
        "Goûter": {"Matin": "-", "Midi": "-", "Après-midi": "S", "Soir": "-"},
    },
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
    },
    "services": ["Terrasse"],
    "tags": ["Torréfaction Artisanale", "Café de Spécialité", "Façade Bois", "Quartier Camas", "Sous l'Arbre"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2019/09/Brulerie-Moka_Torrefaction-Marseille_Love-Spots_08.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2019/09/Brulerie-Moka_Torrefaction-Marseille_Love-Spots_05.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2019/09/Brulerie-Moka_Torrefaction-Marseille_Love-Spots_04.jpg",
    ],
})

# ---------- Le Petit Café ----------
lieux.append({
    "nom": "Le Petit Café",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Café"],
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Corderie",
    "adresse": "Place de la Corderie, 13006 Marseille",
    "latitude": 43.2865,
    "longitude": 5.3745,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": None,
    "telephone_public": None,
    "niveau_engagement": None,
    "gamme_prix": "€",
    "cadre": "Mixte",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (27/02/2023). Adresse précise (numéro de rue) "
        "non trouvée en ligne, seule la place est mentionnée - à affiner. Aucun téléphone public "
        "trouvé."
    ),
    "horaires": {
        "Lundi": [("07:00", "19:00")],
        "Mardi": [("07:00", "19:00")],
        "Mercredi": [("07:00", "19:00")],
        "Jeudi": [("07:00", "19:00")],
        "Vendredi": [("07:00", "19:00")],
        "Samedi": [("07:00", "14:00")],
        "Dimanche": None,
    },
    "phrases_accroche": {
        "Matin": "Un café pressé du matin transformé en vraie pause grâce à la bonne humeur du patron.",
        "Midi": "Le rendez-vous de quartier pour un café ou une formule petit-déjeuner tardive.",
        "Après-midi": "Une pause conviviale en terrasse, entre habitués du quartier.",
        "Soir": "Derniers cafés avant la fermeture, dans une ambiance de fin de journée tranquille.",
    },
    "contact": None,
    "activites_priorite": {
        "Boire un café": {"Matin": "P", "Midi": "S", "Après-midi": "S", "Soir": "S"},
    },
    "ambiance": {
        "Matin": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Soir": {"bruit": "Faible", "luminosite": "Faible", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
    },
    "services": ["Terrasse"],
    "tags": ["Café de Quartier", "Pas Cher", "Ambiance Familiale", "Habitués", "Bonne Humeur"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2023/02/Le-Petit-Cafe_Marseille_City-Guide_Love-Spots_03.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2023/02/Le-Petit-Cafe_Marseille_City-Guide_Love-Spots_02.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2023/02/Le-Petit-Cafe_Marseille_City-Guide_Love-Spots_05.jpg",
    ],
})

# ---------- Mañana ----------
lieux.append({
    "nom": "Mañana",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Café"],
    "code_postal": "13007",
    "arrondissement": "7e",
    "quartier": "Saint-Victor",
    "adresse": "120 boulevard de la Corderie, 13007 Marseille",
    "latitude": 43.2884,
    "longitude": 5.3641,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": None,
    "telephone_public": "06 63 64 67 27",
    "niveau_engagement": None,
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (27/02/2026), Instagram @manana_marseille. "
        "Café de quartier de tradition ibérique tenu par Diane, François et Laurent."
    ),
    "horaires": {
        "Lundi": None,
        "Mardi": [("07:00", "17:30")],
        "Mercredi": [("07:00", "17:30")],
        "Jeudi": [("07:00", "17:30")],
        "Vendredi": [("07:00", "17:30")],
        "Samedi": [("07:00", "17:30")],
        "Dimanche": [("07:00", "17:30")],
    },
    "phrases_accroche": {
        "Matin": "Petit-déjeuner façon café olé, entre spécialités espagnoles et cafés soignés.",
        "Midi": "Une pause méridionale ensoleillée à deux pas de Saint-Victor.",
        "Après-midi": "Un goûter ibérique dans une ambiance ultra cosy.",
        "Soir": None,
    },
    "contact": None,
    "activites_priorite": {
        "Boire un café": {"Matin": "P", "Midi": "S", "Après-midi": "P", "Soir": "-"},
        "Manger": {"Matin": "S", "Midi": "P", "Après-midi": "-", "Soir": "-"},
    },
    "ambiance": {
        "Matin": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
    },
    "services": ["Terrasse"],
    "tags": ["Café Olé", "Tradition Ibérique", "Cosy", "Quartier Saint-Victor", "Spécialités Espagnoles"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2026/02/manana_cafe-de-quartier_marseille_love-spots_05.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/02/manana_cafe-de-quartier_marseille_love-spots_19-1.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/02/manana_cafe-de-quartier_marseille_love-spots_16.jpeg",
    ],
})

ids = []
for data in lieux:
    lid = add_lieu(data)
    ids.append((lid, data["nom"]))
    print("Inséré :", lid, data["nom"])

print(ids)
