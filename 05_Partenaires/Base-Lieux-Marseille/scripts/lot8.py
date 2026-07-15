import sys
sys.path.insert(0, '/tmp/lieux_db')
from lieu_helper import add_lieu

STRUCT_9 = ["Lire", "Travailler", "Jeux de société", "Jeux vidéos", "Écouter de la musique",
            "Manger", "Boire un verre", "Boire un café", "Goûter"]

def base_activites(sourced: dict) -> dict:
    out = {}
    for act in STRUCT_9:
        out[act] = {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"}
    for act, moments in sourced.items():
        if act not in out:
            out[act] = {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"}
        out[act].update(moments)
    return out

LIEUX = []

# 1. T65
LIEUX.append({
    "nom": "T65",
    "types": ["Boulangerie"],
    "code_postal": "13007",
    "arrondissement": "7e",
    "quartier": "Endoume",
    "adresse": "35 Avenue de la Corse, 13007 Marseille",
    "site_web": "http://www.instagram.com/t65boulangerie",
    "telephone_public": "04 96 17 41 33",
    "gamme_prix": "€",
    "cadre": "Intérieur",
    "source_donnees": "love-spots.com (19/08/2022, https://marseille.love-spots.com/en/spots/eating-out/bakery/178584-t65.html) : boulangerie artisanale à Endoume, farines bio, levain naturel, blés anciens. Ouvert mardi-samedi 07h30-19h30, dimanche 07h30-14h00 (fermé lundi). Focaccia 3,90€, sandwichs dès 6,50€, pain 6€/kg. Tél 04 96 17 41 33. Instagram @t65boulangerie. Recoupement WebSearch (2025, Time Out, Les Marseillaises, avis Google) : toujours en activité en 2025-2026, ouverte en 2022 par Ambre Baker et Virgile Arlaud. 3 images HD réelles (galerie love-spots).",
    "horaires": {
        "Lundi": None,
        "Mardi": [("07:30", "19:30")], "Mercredi": [("07:30", "19:30")], "Jeudi": [("07:30", "19:30")],
        "Vendredi": [("07:30", "19:30")], "Samedi": [("07:30", "19:30")],
        "Dimanche": [("07:30", "14:00")],
    },
    "activites_priorite": base_activites({
        "Manger": {"Matin": "S", "Midi": "P"},
        "Goûter": {"Après-midi": "P"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Non applicable", "affluence": "Modéré", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Non applicable", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Non applicable", "affluence": "Modéré", "types": ["Calme"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
    },
    "services": [],
    "tags": ["artisan", "bakery", "gluten-free", "healthy wheat", "natural yeast", "Organic flours", "With kids", "Endoume"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2022/08/T65_boulangerie_Marseille_City-Guide_Love-Spots_02.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2022/08/T65_boulangerie_Marseille_City-Guide_Love-Spots_05.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2022/08/T65_boulangerie_Marseille_City-Guide_Love-Spots_08.jpg",
    ],
})

# 2. Maison Geney
LIEUX.append({
    "nom": "Maison Geney",
    "types": ["Boulangerie", "Café"],
    "code_postal": "13002",
    "arrondissement": "2e",
    "quartier": "Panier",
    "adresse": "38 Rue Caisserie, 13002 Marseille",
    "site_web": "http://www.facebook.com/maisongeney",
    "telephone_public": "04 91 52 44 82",
    "gamme_prix": "€",
    "cadre": "Mixte",
    "source_donnees": "love-spots.com (20/01/2016, https://marseille.love-spots.com/en/spots/eating-out/bakery-tearoom/76219-maison-geney.html) : salon de thé-traiteur près de l'Hôtel de Ville/Panier, tarte 4,50€, salade 6,50€, plat chaud 7,90€. Tél 04 91 52 44 82. Horaires 2016 : mardi-dimanche 8h-19h30. ATTENTION discrepancy : sources récentes agrégées (Yelp 18 avis 4.5/5, Tripadvisor, Marseille Tourisme, Divento — tous 2025-2026) indiquent des horaires actualisés lundi-samedi 10h-16h30 (fermé dimanche), ouvert en 2015 par l'ex-Top Chef Étienne Geney et son épouse Manon. Horaires 2025-2026 retenus comme plus fiables (plus récents, multi-sources concordantes) ; horaires 2016 conservés ici à titre de trace. Vérifié : lieu toujours en activité en 2026, pas de renommage en 'Maison Charlie' (établissement distinct et non lié). 3 images HD réelles (galerie love-spots).",
    "horaires": {
        "Lundi": [("10:00", "16:30")], "Mardi": [("10:00", "16:30")], "Mercredi": [("10:00", "16:30")],
        "Jeudi": [("10:00", "16:30")], "Vendredi": [("10:00", "16:30")], "Samedi": [("10:00", "16:30")],
        "Dimanche": None,
    },
    "activites_priorite": base_activites({
        "Manger": {"Midi": "P"},
        "Boire un café": {"Matin": "S"},
        "Goûter": {"Après-midi": "S"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Modéré", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
    },
    "services": ["Terrasse", "Wifi"],
    "tags": ["cantine", "traiteur", "produits frais", "plats à emporter", "Panier", "Best Of"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2016/01/Love-spots_Marseille_Maison-Geney_03.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2016/01/Love-spots_Marseille_Maison-Geney_02.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2016/01/Love-spots_Marseille_Maison-Geney_04.jpg",
    ],
})

# 3. Oh Faon
LIEUX.append({
    "nom": "Oh Faon",
    "types": ["Boulangerie", "Café"],
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Préfecture",
    "adresse": "2 Rue Edmond Rostand, 13006 Marseille",
    "site_web": "http://www.ohfaon.com",
    "telephone_public": "06 50 84 94 67",
    "gamme_prix": "€",
    "cadre": "Intérieur",
    "source_donnees": "love-spots.com (14/09/2018, https://marseille.love-spots.com/en/spots/eating-out/bakery-tearoom/99637-oh-faon.html) : pâtisserie végétale (vegan) et sans gluten dans le quartier des Antiquaires/Préfecture, tartelettes/cookies/bars 4,50-5,50€, ouvert 2018 par Jérôme Raffaelli et Kevin Yau. Horaires 2018 : mardi-samedi 9h-14h30 et 15h30-19h (coupure méridienne). Recoupement WebSearch (2025, HappyCow, avis 5/5) : horaires actualisés mardi-samedi 9h30-19h en continu, dimanche 10h-17h (élargissement à l'ouverture dominicale depuis 2018). Horaires 2025 retenus comme plus récents. Tél 06 50 84 94 67. Site ohfaon.com. 3 images HD réelles (galerie love-spots).",
    "horaires": {
        "Lundi": None,
        "Mardi": [("09:30", "19:00")], "Mercredi": [("09:30", "19:00")], "Jeudi": [("09:30", "19:00")],
        "Vendredi": [("09:30", "19:00")], "Samedi": [("09:30", "19:00")],
        "Dimanche": [("10:00", "17:00")],
    },
    "activites_priorite": base_activites({
        "Goûter": {"Matin": "S", "Après-midi": "P"},
        "Boire un café": {"Matin": "S", "Après-midi": "S"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Modéré", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
    },
    "services": [],
    "tags": ["vegan", "gluten-free", "Artisanal", "cookies", "lemon pie", "banana bread", "quartier des antiquaires"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2018/09/Patisserie-Vegetale-marseille_Oh-Faon_Love-spots_10.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2018/08/Patisserie-Vegetale-marseille_Oh-Faon_Love-spots_06.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2018/08/Patisserie-Vegetale-marseille_Oh-Faon_Love-spots_02.jpg",
    ],
})

# 4. Café de l'Abbaye
LIEUX.append({
    "nom": "Café de l'Abbaye",
    "types": ["Bar", "Café", "Restaurant"],
    "code_postal": "13007",
    "arrondissement": "7e",
    "quartier": "Saint-Victor",
    "adresse": "3 rue d'Endoume, 13007 Marseille",
    "telephone_public": "04 91 66 87 57",
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": "love-spots.com (26/10/2010, https://marseille.love-spots.com/adresses/ou-sortir/bars-marseille/298-cafe-de-labbaye.html) : bar/café-restaurant à Endoume/Saint-Victor, vue sur le Fort Saint-Jean, plat du jour ~10€, service au comptoir, terrasse triangulaire prisée à l'apéro. Tél d'origine (2010) 04 91 33 44 67, horaires d'origine lundi-vendredi 8h30-22h30, samedi-dimanche 15h30-22h30. ATTENTION discrepancy : recoupement WebSearch (2026, Yelp 37 avis, Tripadvisor, My Little Marseille) donne un tél actualisé 04 91 66 87 57 et des horaires actualisés lundi-samedi 9h-22h, dimanche 16h-22h. Les deux jeux d'horaires/tél sont documentés ici ; la version 2026 est retenue comme plus fiable (plus récente, sources multiples concordantes). Seule 1 image HD trouvée (og:image love-spots, pas d'autre image en galerie) — shortfall documenté.",
    "horaires": {
        "Lundi": [("09:00", "22:00")], "Mardi": [("09:00", "22:00")], "Mercredi": [("09:00", "22:00")],
        "Jeudi": [("09:00", "22:00")], "Vendredi": [("09:00", "22:00")], "Samedi": [("09:00", "22:00")],
        "Dimanche": [("16:00", "22:00")],
    },
    "activites_priorite": base_activites({
        "Manger": {"Midi": "P"},
        "Boire un café": {"Matin": "S"},
        "Boire un verre": {"Soir": "P"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Fort", "luminosite": "Modéré", "musique": "Modéré", "affluence": "Fort", "types": ["Dynamique", "Sociable"]},
    },
    "services": ["Terrasse"],
    "tags": ["apéro", "cuisine provençale", "cuisine familiale", "vue Vieux-Port", "Saint-Victor", "good deal"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2010/10/cafe-de-l-abbaye_love-spots-marseille_01.jpg",
    ],
})

# 5. Les Succulentes
LIEUX.append({
    "nom": "Les Succulentes",
    "types": ["Café"],
    "code_postal": "13006",
    "arrondissement": "6e",
    "quartier": "Vauban",
    "adresse": "16 Boulevard Vauban, 13006 Marseille",
    "site_web": "http://www.facebook.com/succulentes.cafe/",
    "telephone_public": "04 65 85 52 42",
    "gamme_prix": "€",
    "cadre": "Intérieur",
    "source_donnees": "love-spots.com (15/03/2018, https://marseille.love-spots.com/en/spots/eating-out/cafe-en/94821-les-succulentes.html) : café à thème cactus dans le haut Breteuil/Vauban, formule bun/sandwich+boisson+dessert 10-12,50€, café 1,80€, thé/infusion 3€. Bus 57 arrêt Vauban Breteuil. Tél 04 65 85 52 42. Ouvert lundi-vendredi 8h30-18h, samedi 9h30-17h30 (fermé dimanche) — 'impossible de s'asseoir aux heures de pointe'. Toujours référencé activement par love-spots.com en 2026 (catégorie 'Cafes' à jour). 3 images HD réelles (galerie love-spots).",
    "horaires": {
        "Lundi": [("08:30", "18:00")], "Mardi": [("08:30", "18:00")], "Mercredi": [("08:30", "18:00")],
        "Jeudi": [("08:30", "18:00")], "Vendredi": [("08:30", "18:00")],
        "Samedi": [("09:30", "17:30")], "Dimanche": None,
    },
    "activites_priorite": base_activites({
        "Boire un café": {"Matin": "P"},
        "Manger": {"Midi": "S"},
        "Goûter": {"Après-midi": "S"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Midi": {"bruit": "Fort", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
    },
    "services": [],
    "tags": ["cactus", "Breakfast", "gluten-free", "Homemade", "salad", "soup", "tartines", "vauban", "Take away"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2018/02/Cafe-cactus_Marseille_Les-Succulentes_Love-Spots_01.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2018/02/Cafe-cactus_Marseille_Les-Succulentes_Love-Spots_05.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2018/02/Cafe-cactus_Marseille_Les-Succulentes_Love-Spots_02.jpg",
    ],
})

# 6. Deïa Coffee & Kitchen
LIEUX.append({
    "nom": "Deïa Coffee & Kitchen",
    "types": ["Restaurant", "Café"],
    "code_postal": "13001",
    "arrondissement": "1er",
    "quartier": "Opéra",
    "adresse": "1A Rue Molière, 13001 Marseille",
    "site_web": "http://www.instagram.com/deiamarseille",
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": "love-spots.com (21/06/2024, https://marseille.love-spots.com/en/spots/eating-out/restaurants/207992-deia-coffee-kitchen.html) : brunch chic dans le quartier Opéra, à 20m de son emplacement d'origine. Pancakes 12,50€, eggs Benedict 14,90€, latte signature antioxydant 5,50€. Ouvert lundi-vendredi 9h-16h, samedi-dimanche 8h30-16h30. Métro Vieux-Port. Contact email deia.coffee.kitcheb@gmail.com (orthographe telle que publiée par la source, possible coquille de l'établissement lui-même). Pas de téléphone public trouvé. 3 images HD réelles (galerie love-spots).",
    "horaires": {
        "Lundi": [("09:00", "16:00")], "Mardi": [("09:00", "16:00")], "Mercredi": [("09:00", "16:00")],
        "Jeudi": [("09:00", "16:00")], "Vendredi": [("09:00", "16:00")],
        "Samedi": [("08:30", "16:30")], "Dimanche": [("08:30", "16:30")],
    },
    "activites_priorite": base_activites({
        "Manger": {"Matin": "P", "Midi": "P"},
        "Boire un café": {"Matin": "P"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Midi": {"bruit": "Fort", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Faible", "luminosite": "Modéré", "musique": "Faible", "affluence": "Faible", "types": ["Calme"]},
        "Soir": {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": ["Calme"]},
    },
    "services": ["Terrasse"],
    "tags": ["brunch", "opéra", "terrace", "restaurant", "café"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2024/06/Deia_Brunch_Healthy_Restaurant_-_Marseille_Love_spots_17.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2024/06/Deia_Brunch_Healthy_Restaurant_-_Marseille_Love_spots_09-scaled.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2024/06/Deia_Brunch_Healthy_Restaurant_-_Marseille_Love_spots_07-scaled.jpeg",
    ],
})

# 7. Café de la Consigne
LIEUX.append({
    "nom": "Café de la Consigne",
    "types": ["Bar", "Café"],
    "code_postal": "13002",
    "arrondissement": "2e",
    "quartier": "Vieux-Port",
    "adresse": "3 quai du Port, 13002 Marseille",
    "site_web": "http://www.instagram.com/cafe.de.la.consigne/",
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": "love-spots.com (25/03/2026, https://marseille.love-spots.com/en/spots/eating-out/cafe-en/238133-la-cafe-de-la-consigne.html) : bar et cantine installés dans l'ancienne consigne sanitaire du Vieux-Port, face au Fort Saint-Jean et au Mucem, bâtiment historique longtemps fermé au public. Formule petit-déjeuner 10€, assiettes 5,50-18€, affogato 7€, verre de vin 6,50€. Horaires : lundi-jeudi 10h-18h30, vendredi et samedi 10h-23h, dimanche 10h-22h30 (heure d'ouverture du dimanche non précisée explicitement par la source, alignée par défaut sur les autres jours à 10h). Métro Vieux-Port. Pas de téléphone public trouvé, contact via Instagram @cafe.de.la.consigne. Source très récente (mars 2026), pas de discrepancy identifiée. 3 images HD réelles (galerie love-spots).",
    "horaires": {
        "Lundi": [("10:00", "18:30")], "Mardi": [("10:00", "18:30")], "Mercredi": [("10:00", "18:30")],
        "Jeudi": [("10:00", "18:30")],
        "Vendredi": [("10:00", "23:00")], "Samedi": [("10:00", "23:00")],
        "Dimanche": [("10:00", "22:30")],
    },
    "activites_priorite": base_activites({
        "Boire un café": {"Matin": "S"},
        "Manger": {"Midi": "S"},
        "Boire un verre": {"Soir": "P"},
    }),
    "ambiance": {
        "Matin": {"bruit": "Faible", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Calme"]},
        "Midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Fort", "types": ["Sociable"]},
        "Après-midi": {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir": {"bruit": "Fort", "luminosite": "Modéré", "musique": "Modéré", "affluence": "Fort", "types": ["Dynamique", "Sociable"]},
    },
    "services": ["Terrasse"],
    "tags": ["apéro", "breakfast", "Vieux-Port", "patrimoine", "terrasse"],
    "images": [
        "https://marseille.love-spots.com/wp-content/uploads/2026/03/Le-Cafe-de-la-Consigne_Bar-et-cantine_Marseille_01.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/03/Le-Cafe-de-la-Consigne_Bar-et-cantine_Marseille_02.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/03/Le-Cafe-de-la-Consigne_Bar-et-cantine_Marseille_03.jpeg",
    ],
})

for L in LIEUX:
    L["partenaire"] = False
    L["lieu_actif"] = True
    lid = add_lieu(L)
    print(f"Inséré : {L['nom']} -> id {lid}")
