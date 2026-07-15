import sys
sys.path.insert(0, '/tmp/lieux_db')
from lieu_helper import add_lieu

STRUCT_9 = ["Lire", "Travailler", "Jeux de société", "Jeux vidéos", "Écouter de la musique",
            "Manger", "Boire un verre", "Boire un café", "Goûter"]

def base_activites(sourced: dict) -> dict:
    """sourced: {activite: {moment: valeur}} -> merge avec défauts '-' pour les 9 structurelles
    (le backfill fill_activites_structurelles.py complètera aussi les manquantes après coup,
    mais on part propre ici)."""
    out = {}
    for act in STRUCT_9:
        out[act] = {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"}
    for act, moments in sourced.items():
        if act not in out:
            out[act] = {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"}
        out[act].update(moments)
    return out

LIEUX = []

# 1. Maison Nosh
LIEUX.append({
    "nom": "Maison Nosh",
    "types": ["Café", "Restaurant"],
    "code_postal": "13001",
    "arrondissement": "1er",
    "quartier": "Vieux-Port",
    "adresse": "20 place aux Huiles, 13001 Marseille",
    "site_web": "http://www.maison-nosh.com/",
    "telephone_public": "06 72 38 95 38",
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": "love-spots.com (11/03/2026, https://marseille.love-spots.com/en/spots/eating-out/cafe-en/236642-maison-nosh.html) : coffee shop/brunch/lunch/goûter, Place aux Huiles, ouvert du mercredi au dimanche 08h-18h (fermé lundi-mardi). Formule à partir de 26,90€, salé dès 9,90€, sucré dès 8,50€. Tél 06 72 38 95 38. Site officiel maison-nosh.com. 3 images HD réelles (og:image + galerie love-spots).",
    "horaires": {
        "Lundi": None, "Mardi": None,
        "Mercredi": [("08:00", "18:00")], "Jeudi": [("08:00", "18:00")],
        "Vendredi": [("08:00", "18:00")], "Samedi": [("08:00", "18:00")],
        "Dimanche": [("08:00", "18:00")],
    },
    "activites_priorite": base_activites({
        "Boire un café": {"Matin": "P", "Midi": "S", "Après-midi": "S"},
        "Manger": {"Midi": "P"},
        "Goûter": {"Après-midi": "P"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Faible", "luminosite": "Faible", "musique": "Non applicable", "affluence": "Faible", "types": ["Calme"]},
    },
    "services": ["Terrasse", "Wifi"],
    "tags": ["brunch", "Ouvert le dimanche", "Place aux Huiles", "Snacks", "Cafés de spécialité", "Terrasse"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2026/03/maison-nosh_brunch_marseille_love-spots_05.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/03/maison-nosh_brunch_marseille_love-spots_13.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/03/maison-nosh_brunch_marseille_love-spots_10.jpg",
    ],
})

# 2. Pain Salvator
LIEUX.append({
    "nom": "Pain Salvator",
    "types": ["Boulangerie", "Café"],
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Préfecture",
    "adresse": "32 Boulevard Louis Salvator, 13006 Marseille",
    "site_web": "http://www.facebook.com/painsalvator/",
    "telephone_public": "06 80 25 11 89",
    "gamme_prix": "€",
    "cadre": "Mixte",
    "source_donnees": "love-spots.com (01/04/2019, https://marseille.love-spots.com/en/spots/eating-out/bakery-tearoom/102583-pain-salvator.html) : boulangerie bio au levain naturel, entre Préfecture et Notre-Dame-du-Mont, ouvert mercredi-vendredi 11h-19h et samedi 10h-14h (fermé dim-mar selon l'article). Pain de campagne 4,90€/kg, café bio 1,50€, brioche au beurre 1,90€/kg. Tél 06 80 25 11 89. Boissons et petites collations bio sur place, en intérieur ou en terrasse.",
    "horaires": {
        "Lundi": None, "Mardi": None,
        "Mercredi": [("11:00", "19:00")], "Jeudi": [("11:00", "19:00")], "Vendredi": [("11:00", "19:00")],
        "Samedi": [("10:00", "14:00")], "Dimanche": None,
    },
    "activites_priorite": base_activites({
        "Boire un café": {"Matin": "S", "Midi": "S"},
        "Goûter": {"Midi": "S", "Après-midi": "S"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Non applicable", "affluence": "Modéré", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Non applicable", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Non applicable", "affluence": "Faible", "types": ["Calme"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
    },
    "services": ["Terrasse"],
    "tags": ["Best Of", "café", "Sans gluten", "Notre-Dame-du-Mont", "Boulangerie bio", "Vin bio", "Préfecture", "Rue Salvator", "Pain au levain", "Thé", "Boulangerie traditionnelle"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2019/04/Boulangerie-Bio-Marseille_Pain-Salvator_Love-spots_01.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2019/04/Boulangerie-Bio-Marseille_Pain-Salvator_Love-spots_04.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2019/04/Boulangerie-Bio-Marseille_Pain-Salvator_Love-spots_03.jpg",
    ],
})

# 3. La Caravelle
LIEUX.append({
    "nom": "La Caravelle",
    "types": ["Bar", "Restaurant"],
    "code_postal": "13002",
    "arrondissement": "2e",
    "quartier": "Vieux-Port",
    "adresse": "34 Quai du Port, 13002 Marseille",
    "site_web": "http://www.lacaravelle-marseille.com",
    "telephone_public": "04 96 17 05 40",
    "gamme_prix": "€€",
    "cadre": "Intérieur",
    "source_donnees": "love-spots.com (15/12/2013, https://marseille.love-spots.com/en/spots/out-about-spots/68852-la-caravelle-2.html) : bar de l'hôtel Bellevue, 34 Quai du Port, cocktails/tapas, concerts jazz. L'article original donne des horaires visiblement erronés/obsolètes (\"everyday 7am to 2pm\"). Recoupé et corrigé via le site officiel hotelbellevuemarseille.com/en/le-bar (màj 12/03/2025) qui décrit le bar ouvert tous les jours en 3 temps : apéritif 18h30-21h, cocktails 21h-23h, \"sirènes de la nuit\" 23h-2h — soit environ 18h30-02h tous les jours. Concerts jazz mercredi et vendredi soir (source secondaire WebSearch). Téléphone hôtel 04 96 17 05 40 (source officielle, remplace l'ancien 04 91 90 36 64 de l'article 2013). Une seule image HD trouvée (og:image love-spots) ; le site officiel n'expose pas d'URL d'image directement exploitable (chargement JS) — 2 images manquantes, à rechercher ultérieurement.",
    "horaires": {
        "Lundi": [("18:30", "02:00")], "Mardi": [("18:30", "02:00")], "Mercredi": [("18:30", "02:00")],
        "Jeudi": [("18:30", "02:00")], "Vendredi": [("18:30", "02:00")], "Samedi": [("18:30", "02:00")],
        "Dimanche": [("18:30", "02:00")],
    },
    "activites_priorite": base_activites({
        "Boire un verre": {"Soir": "P"},
        "Manger": {"Soir": "S"},
        "Écouter de la musique": {"Soir": "S"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
        "Midi": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Soir": {"bruit": "Modéré", "luminosite": "Faible", "musique": "Modéré", "affluence": "Fort", "types": ["Sociable", "Dynamique"]},
    },
    "services": ["Wifi"],
    "tags": ["Cocktails", "Vieux-Port", "Open Monday evening", "Open Sunday evening", "Tapas", "Concerts jazz"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2013/12/bar_marseille_lovespots_la-caravelle_01.jpg",
    ],
})

# 4. John Silver
LIEUX.append({
    "nom": "John Silver",
    "types": ["Café", "Restaurant"],
    "code_postal": "13001",
    "arrondissement": "1er",
    "quartier": "Vieux-Port",
    "adresse": "6 rue Neuve Sainte-Catherine, 13001 Marseille",
    "site_web": "http://www.instagram.com/johnsilver.ob/",
    "telephone_public": "04 86 68 29 59",
    "gamme_prix": "€€",
    "cadre": "Intérieur",
    "source_donnees": "love-spots.com (02/02/2026, https://marseille.love-spots.com/en/spots/eating-out/fast-food/232348-john-silver.html) : \"bistroffee\" 100% végétal/vegan, à deux pas du Vieux-Port, ouvert mardi-samedi 8h30-16h (fermé dim-lun). Expresso 2€, chaï/ube latte 4,50€, kombucha 5€, plats 15-16€, dessert 6€. Tél 04 86 68 29 59. Pas de site web propre, Instagram @johnsilver.ob.",
    "horaires": {
        "Lundi": None,
        "Mardi": [("08:30", "16:00")], "Mercredi": [("08:30", "16:00")], "Jeudi": [("08:30", "16:00")],
        "Vendredi": [("08:30", "16:00")], "Samedi": [("08:30", "16:00")],
        "Dimanche": None,
    },
    "activites_priorite": base_activites({
        "Boire un café": {"Matin": "P", "Après-midi": "S"},
        "Manger": {"Midi": "P"},
        "Goûter": {"Après-midi": "S"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
    },
    "services": [],
    "tags": ["Coffee Shop", "Végétarien", "Vegan", "Vieux-Port"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2026/01/John-Silver_Bistrot_Coffee-shop_Marseille_Love-Spots_10.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/01/John-Silver_Bistrot_Coffee-shop_Marseille_Love-Spots_05.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/01/John-Silver_Bistrot_Coffee-shop_Marseille_Love-Spots_02.jpeg",
    ],
})

# 5. Ivresse
LIEUX.append({
    "nom": "Ivresse",
    "types": ["Bar", "Cave à vins"],
    "code_postal": "13001",
    "arrondissement": "1er",
    "quartier": "Longchamp",
    "adresse": "76 Rue Léon Bourgeois, 13001 Marseille",
    "site_web": "http://www.instagram.com/ivresse.lacave/",
    "telephone_public": None,
    "gamme_prix": "€",
    "cadre": "Intérieur",
    "source_donnees": "love-spots.com (21/12/2022, https://marseille.love-spots.com/en/spots/out-about-spots/bars-en/180990-ivresse.html) : cave et bar à vins nature installé dans un ancien garage, quartier Longchamp, ouvert mardi-samedi 16h-23h (fermé dim-lun). Verre de vin 5€, petits plats 6-10€, bouteilles à emporter 12-40€, droit de bouchon 7€. Pas de téléphone public communiqué dans l'article (Instagram uniquement). Point ouvert : l'adresse (13001) et le tag \"Longchamp\" (quartier généralement rattaché au 4e arrondissement) semblent en léger désaccord — donnée reprise telle quelle depuis la source primaire, à vérifier.",
    "horaires": {
        "Lundi": None,
        "Mardi": [("16:00", "23:00")], "Mercredi": [("16:00", "23:00")], "Jeudi": [("16:00", "23:00")],
        "Vendredi": [("16:00", "23:00")], "Samedi": [("16:00", "23:00")],
        "Dimanche": None,
    },
    "activites_priorite": base_activites({
        "Boire un verre": {"Après-midi": "S", "Soir": "P"},
        "Manger": {"Soir": "S"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
        "Midi": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Soir": {"bruit": "Modéré", "luminosite": "Faible", "musique": "Modéré", "affluence": "Modéré", "types": ["Sociable"]},
    },
    "services": [],
    "tags": ["Bar", "Best Of", "Longchamp", "Bar à vin", "Cave à vins", "Vins nature"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2022/11/Ivresse_Cave-et-Bar-a-vins-nature_Marseille_City-guide_Love-spots_03.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2022/11/Ivresse_Cave-et-Bar-a-vins-nature_Marseille_City-guide_Love-spots_05.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2022/11/Ivresse_Cave-et-Bar-a-vins-nature_Marseille_City-guide_Love-spots_08.jpeg",
    ],
})

# 6. Bistrot Margaux
LIEUX.append({
    "nom": "Bistrot Margaux",
    "types": ["Bar", "Cave à vins"],
    "code_postal": "13004",
    "arrondissement": "4e",
    "quartier": "Les 5 Avenues",
    "adresse": "25 Boulevard Philippon, 13004 Marseille",
    "site_web": "http://www.facebook.com/Bistrot-Margaux-1658564331068964/",
    "telephone_public": "09 54 29 87 65",
    "gamme_prix": "€",
    "cadre": "Mixte",
    "source_donnees": "love-spots.com (08/05/2016, https://marseille.love-spots.com/en/spots/eating-out/wine-and-beer-cellar/78631-bistrot-margaux.html) : cave à vins et traiteur, produits du Sud-Ouest et de Corse, terrasse sous les platanes, ouvert mardi-samedi 10h30-20h30 et dimanche matin 10h30-13h (fermé lundi). Verre de vin 4-6€, planche fromages/charcuterie 12€, formule déjeuner (plat du jour + dessert + café) 12,90€. Tél 09 54 29 87 65.",
    "horaires": {
        "Lundi": None,
        "Mardi": [("10:30", "20:30")], "Mercredi": [("10:30", "20:30")], "Jeudi": [("10:30", "20:30")],
        "Vendredi": [("10:30", "20:30")], "Samedi": [("10:30", "20:30")],
        "Dimanche": [("10:30", "13:00")],
    },
    "activites_priorite": base_activites({
        "Boire un verre": {"Après-midi": "P", "Soir": "S"},
        "Manger": {"Midi": "P"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Non applicable", "affluence": "Faible", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Modéré", "luminosite": "Modéré", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
    },
    "services": ["Terrasse", "Vente à emporter"],
    "tags": ["Apéro", "Produits artisanaux", "Best Of", "Groupes", "Ouvert le dimanche", "Vente à emporter", "Tapas", "Terrasse", "Bar à vin", "Vins"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2016/05/Bar-a-Vins_Marseille_Bistrot-Margaux_Love-spots_01.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2016/05/Bar-a-Vins_Marseille_Bistrot-Margaux_Love-spots_04.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2016/05/Bar-a-Vins_Marseille_Bistrot-Margaux_Love-spots_02.jpg",
    ],
})

# 7. Pain Pan
LIEUX.append({
    "nom": "Pain Pan",
    "types": ["Boulangerie"],
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Cours Julien / La Plaine",
    "adresse": "29 Rue 3 Frères Barthélémy, 13006 Marseille",
    "site_web": "http://www.facebook.com/BoulangeriePAINPAN/",
    "telephone_public": "06 15 44 75 45",
    "gamme_prix": "€",
    "cadre": "Intérieur",
    "source_donnees": "love-spots.com (22/01/2020, https://marseille.love-spots.com/en/spots/eating-out/bakery/107956-pain-pan.html) : boulangerie artisanale bio, entre Cours Julien et La Plaine, ouvert mardi-samedi 7h30-20h30 et dimanche 7h30-13h30 (fermé lundi). Pain de campagne 4,90€/kg, baguette au levain 1,20€, pain choco-noisette 1,60€. Tél 06 15 44 75 45.",
    "horaires": {
        "Lundi": None,
        "Mardi": [("07:30", "20:30")], "Mercredi": [("07:30", "20:30")], "Jeudi": [("07:30", "20:30")],
        "Vendredi": [("07:30", "20:30")], "Samedi": [("07:30", "20:30")],
        "Dimanche": [("07:30", "13:30")],
    },
    "activites_priorite": base_activites({
        "Goûter": {"Matin": "S", "Après-midi": "S"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Non applicable", "affluence": "Fort", "types": ["Sociable"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Non applicable", "affluence": "Modéré", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Non applicable", "affluence": "Faible", "types": ["Calme"]},
        "Soir": {"bruit": "Faible", "luminosite": "Faible", "musique": "Non applicable", "affluence": "Faible", "types": ["Calme"]},
    },
    "services": [],
    "tags": ["Artisanal", "Boulangerie", "Best Of"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2019/12/Pain-Pan_Boulangerie-artisanale_Marseille_Love-spots_06.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2019/12/Pain-Pan_Boulangerie-artisanale_Marseille_Love-spots_04.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2019/12/Pain-Pan_Boulangerie-artisanale_Marseille_Love-spots_05.jpg",
    ],
})

# 8. Le Molotov
LIEUX.append({
    "nom": "Le Molotov",
    "types": ["Bar"],
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Cours Julien",
    "adresse": "3 place Paul Cézanne, 13006 Marseille",
    "site_web": "https://lemolotov.com/",
    "telephone_public": None,
    "gamme_prix": "€",
    "cadre": "Intérieur",
    "source_donnees": "love-spots.com (24/08/2012, https://marseille.love-spots.com/en/spots/out-about-spots/70091-molotov.html) : salle de concert (rock/reggae/hip-hop/jazz/electro), Cours Julien, ouvert mardi-dimanche 18h-1h30 (fermé lundi), entrée 10€ hors concerts/évènements spéciaux. Recoupé et confirmé toujours en activité via le site officiel lemolotov.com (programmation 2026 très dense, concerts quasi quotidiens de juillet à décembre 2026) — lieu bien réel et actif malgré la source principale ancienne (2012). Pas de téléphone communiqué. Il s'agit avant tout d'une salle de concert/spectacle plutôt que d'un bar/café/restaurant classique ; classé ici comme \"Bar\" par défaut (pas de type \"salle de concert\" dans le référentiel), l'activité \"Écouter de la musique\" reflète mieux sa vocation première.",
    "horaires": {
        "Lundi": None,
        "Mardi": [("18:00", "01:30")], "Mercredi": [("18:00", "01:30")], "Jeudi": [("18:00", "01:30")],
        "Vendredi": [("18:00", "01:30")], "Samedi": [("18:00", "01:30")],
        "Dimanche": [("18:00", "01:30")],
    },
    "activites_priorite": base_activites({
        "Écouter de la musique": {"Soir": "P"},
        "Boire un verre": {"Soir": "P"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
        "Midi": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Faible", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Soir": {"bruit": "Fort", "luminosite": "Faible", "musique": "Fort", "affluence": "Fort", "types": ["Dynamique"]},
    },
    "services": [],
    "tags": ["Cours Julien", "Open Sunday evening", "Salle de concert", "Musiques actuelles"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2012/08/salle-de-concerts-marseille-molotov-lovespots-1.jpg",
        "http://lemolotov.com/wp-content/uploads/2019/08/lemolotovmarseille.jpg",
    ],
})

# 9. Mercato by Winesucker
LIEUX.append({
    "nom": "Mercato by Winesucker",
    "types": ["Bar", "Cave à vins", "Restaurant"],
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Notre-Dame-du-Mont",
    "adresse": "36 Rue de la Loubière, 13006 Marseille",
    "site_web": "https://instagram.com/mercato_winesucker",
    "telephone_public": None,
    "note_google": 4.6,
    "nombre_avis_google": 93,
    "gamme_prix": "€€",
    "cadre": "Intérieur",
    "source_donnees": "Pas de fiche love-spots.com dédiée trouvée malgré recherche croisée — sourcé via Mapstr (mapstr.com/place/kNZo1mQCDk, ouvert par Fred Semerdjian en 2024, quartier Notre-Dame-du-Mont, vins nature sans sulfites ajoutés + tapas végétariennes/végétales inspiration japonaise-marseillaise, ambiance tons rouges), restaurants-de-france.fr (36 Rue de la Loubière 13006, note 4,6/5 sur 93 avis synchronisés Google Maps, avis clients cohérents sur cave à vins nature + petites assiettes végé parfois jugées chères) et WebSearch croisé (lefooding.com, restaurant-autour-de-moi.com, pagesjaunes.fr). Horaires lundi-vendredi 18h-23h (fermé samedi-dimanche) confirmés par plusieurs sources indépendantes (dont citations utilisateurs Mapstr). Pas de téléphone public trouvé. 3 images HD réelles issues de la galerie Google Photos via Mapstr (pas d'article love-spots donc pas d'og:image dédiée du site).",
    "horaires": {
        "Lundi": [("18:00", "23:00")], "Mardi": [("18:00", "23:00")], "Mercredi": [("18:00", "23:00")],
        "Jeudi": [("18:00", "23:00")], "Vendredi": [("18:00", "23:00")],
        "Samedi": None, "Dimanche": None,
    },
    "activites_priorite": base_activites({
        "Boire un verre": {"Soir": "P"},
        "Manger": {"Soir": "P"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
        "Midi": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
        "Après-midi": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
        "Soir": {"bruit": "Modéré", "luminosite": "Faible", "musique": "Modéré", "affluence": "Fort", "types": ["Sociable", "Dynamique"]},
    },
    "services": [],
    "tags": ["Bar à vin", "Vins nature", "Cuisine végétale", "Tapas", "Notre-Dame-du-Mont", "Cave à manger"],
    "images": [
        "https://lh3.googleusercontent.com/places/ANJU3DuWEXHuqUrsbKk5i9ZROfxXjdMT3c2Rxrm6DGaf_HTzDTDjQp72ALG7nb4dT_WmXWKM-AUhM3ANcCHiV3X9jyuaaIk7XfvJVYw=s1600-w640",
        "https://lh3.googleusercontent.com/places/ANJU3Dudu1NzbZ6iJcTDqDLV7WpsTCe3lBND29qIrCKekMmiNVn4aPxaaz0v4K_eJ1VXuHzFAkzhMNlwjnFQpyBvy3Csz5XV3f4haB0=s1600-w640",
        "https://lh3.googleusercontent.com/places/ANJU3DtmlUEk3ZXbWflfSYwUQ3LyoaxUk9DA7Q4DV_iMwaJ1jwMWwIz4gfK2MbZkeXcSVg-GXb7aC9BQX8lMdI-meEK4EWajGohjnsw=s1600-w640",
    ],
})

for L in LIEUX:
    L["partenaire"] = False
    L["lieu_actif"] = True
    lid = add_lieu(L)
    print(f"Inséré : {L['nom']} -> id {lid}")
