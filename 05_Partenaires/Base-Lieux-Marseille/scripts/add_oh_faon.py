import sys
sys.path.insert(0, '/tmp/lieux_db')
from lieu_helper import add_lieu, get_lieu_summary

data = {
    "nom": "Oh Faon",
    "lieu_actif": True,
    "types": ["Boulangerie"],
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Préfecture",
    "adresse": "2 Rue Edmond Rostand, 13006 Marseille",
    "site_web": "https://www.ohfaon.com",
    "telephone_public": "06 50 84 94 67",
    "gamme_prix": "€",
    "cadre": "Intérieur",
    "source_donnees": (
        "[2026-07-15] Réinsertion après suppression accidentelle (id 56 supprimé le 15/07/2026 puis redemandé "
        "par l'utilisateur \"remet Oh faon\"). Sources : marseille.love-spots.com (14/09/2018, "
        "https://marseille.love-spots.com/en/spots/eating-out/bakery-tearoom/99637-oh-faon.html) : pâtisserie "
        "artisanale 100% végétale (sans beurre, oeufs ni crème), quartier des Antiquaires/Préfecture, ouverte "
        "novembre 2017 par Jérôme Raffaelli et Kevin Yau. Ouvert mardi-samedi 9h-14h30 et 15h30-19h (fermé "
        "dimanche-lundi), tarifs 4,50-5,50€. Spécialités : Startelette (tarte au citron), Mucho Matcha, Sticky "
        "Mango, banana bread ; option sans gluten disponible (fond noisette/châtaigne). Boutique miniature à "
        "comptoir, places limitées. Tél 06 50 84 94 67, site ohfaon.com. 3 images HD réelles (galerie love-spots, "
        "identiques à l'insertion originale)."
    ),
    "horaires": {
        "Lundi": None,
        "Mardi": [("09:00", "14:30"), ("15:30", "19:00")],
        "Mercredi": [("09:00", "14:30"), ("15:30", "19:00")],
        "Jeudi": [("09:00", "14:30"), ("15:30", "19:00")],
        "Vendredi": [("09:00", "14:30"), ("15:30", "19:00")],
        "Samedi": [("09:00", "14:30"), ("15:30", "19:00")],
        "Dimanche": None,
    },
    "activites_priorite": {
        "Manger": {"Matin": "-", "Midi": "S", "Après-midi": "-", "Soir": "-"},
        "Boire un café": {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Goûter": {"Matin": "-", "Midi": "-", "Après-midi": "P", "Soir": "-"},
        "Boire un verre": {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Lire": {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Travailler": {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Jeux de société": {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Jeux vidéos": {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Écouter de la musique": {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Divertissement": {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
    },
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Dynamique"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Dynamique"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
    },
    "services": ["Vente à emporter", "Options sans gluten", "Vegan"],
    "tags": ["Pâtisserie 100% végétale (sans beurre, oeufs ni crème)", "Tartelette au citron réputée"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2018/09/Patisserie-Vegetale-marseille_Oh-Faon_Love-spots_10.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2018/08/Patisserie-Vegetale-marseille_Oh-Faon_Love-spots_06.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2018/08/Patisserie-Vegetale-marseille_Oh-Faon_Love-spots_02.jpg",
    ],
}

lieu_id = add_lieu(data)
print("Inserted lieu_id =", lieu_id)
print(get_lieu_summary(lieu_id))
