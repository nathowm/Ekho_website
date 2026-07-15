# -*- coding: utf-8 -*-
from lieu_helper import add_lieu

data = {
    "nom": "Chez Moe",
    "partenaire": False,
    "lieu_actif": True,
    "types": ["Café", "Bar"],
    "code_postal": "13002",
    "arrondissement": "2e",
    "quartier": "Panier",
    "adresse": "38 Grand'Rue, 13002 Marseille",
    "latitude": 43.2986,
    "longitude": 5.3697,
    "lien_google_maps": None,
    "note_google": None,
    "nombre_avis_google": None,
    "site_web": "https://www.chezmoe.fr/",
    "telephone_public": None,
    "niveau_engagement": None,
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": (
        "Recherche web 13/07/2026 : love-spots.com (23/08/2024), site officiel chezmoe.fr, "
        "Instagram @chezmoe, recoupement Timeout.fr/Pagesjaunes.fr/Tripadvisor pour confirmer l'adresse. "
        "Coffee shop le jour, bar à vin nature le soir, inspiration japonaise assumée (matchas, iced coffee), "
        "situé au bas du quartier du Panier (tag love-spots 'Hôtel de Ville', zone limitrophe). "
        "Aucun téléphone public trouvé, contact par email (chezmoe.info@gmail.com)."
    ),
    "horaires": {
        "Lundi": None,
        "Mardi": [("09:30", "22:00")],
        "Mercredi": [("09:30", "22:00")],
        "Jeudi": [("09:30", "22:00")],
        "Vendredi": [("09:30", "22:00")],
        "Samedi": [("10:00", "22:00")],
        "Dimanche": None,
    },
    "phrases_accroche": {
        "Matin": "Cafés de compétition et lattes signature pour bien commencer, inspiration japonaise assumée.",
        "Midi": "Sandos, burratina et tielle à savourer sur la terrasse ensoleillée du Grand'Rue.",
        "Après-midi": "Iced coffee et matcha maison pour un goûter dépaysant.",
        "Soir": "Le coffee shop se transforme en bar à vins 100% nature et bières artisanales.",
    },
    "contact": None,
    "activites_priorite": {
        "Boire un café": {"Matin": "P", "Midi": "S", "Après-midi": "S", "Soir": "-"},
        "Boire un verre": {"Matin": "-", "Midi": "-", "Après-midi": "S", "Soir": "P"},
        "Manger": {"Matin": "-", "Midi": "P", "Après-midi": "S", "Soir": "S"},
    },
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Modéré", "luminosite": "Modéré", "musique": "Modéré", "affluence": "Modéré", "types": ["Sociable"]},
    },
    "services": ["Terrasse"],
    "tags": ["Coffee Shop", "Bar à Vin Nature", "Inspiration Japonaise", "Terrasse", "Le Panier"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2024/08/Chez_Moe_cantine_coffee_shop_love_spots_13-scaled.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2024/08/Chez_Moe_cantine_coffee_shop_love_spots_05-scaled.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2024/08/Chez_Moe_cantine_coffee_shop_love_spots_01-scaled.jpeg",
    ],
}

lid = add_lieu(data)
print("Inséré :", lid, data["nom"])
