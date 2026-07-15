import sys
sys.path.insert(0, '/tmp/lieux_db')
from lieu_helper import add_lieu, get_lieu_summary

data = {
    "nom": "Baghera Café",
    "types": ["Café", "Restaurant"],
    "code_postal": "13002",
    "arrondissement": "2e",
    "quartier": "Le Panier",
    "adresse": "29 Grand Rue, 13002 Marseille",
    "site_web": "https://baghera.eatbu.com/",
    "telephone_public": "06 79 78 50 40",
    "note_google": 4.5,
    "nombre_avis_google": 517,
    "gamme_prix": "€€",
    "cadre": "Mixte",
    "source_donnees": (
        "[2026-07-14] VÉRIFIÉ via fetch direct restaurants-de-france.fr "
        "(https://restaurant-brunch.restaurants-de-france.fr/baghera-2061478.html, fiche synchronisée Google Maps, "
        "MAJ 14/10/2025) : adresse 29 Grand Rue 13002 Marseille, note 4.5/5 sur 517 avis, horaires, téléphone "
        "(06 79 78 50 40, confirmé par recoupement WebSearch/Bottin.fr/PagesJaunes), site officiel baghera.eatbu.com. "
        "Bloc 'à propos' plus sommaire que la moyenne (pas de section Ambiance/Clientèle/Points forts sur cette fiche) : "
        "seuls Animaux, Offre (Cafés), Paiements, Parking, Planning (réservations) et Services de restauration/disponibles "
        "renseignés — repris tels quels sans compléter par extrapolation. Menu/spécialités (œufs bénédicte, pancakes "
        "moelleux, avocado toasts, salades gourmandes) et avis clients (assiettes généreuses et copieuses, accueil "
        "chaleureux, un avis mentionne une attente ~10 min le samedi sans réservation et des coussins de terrasse pas "
        "toujours très propres) tirés du texte 'à propos' et des 10 derniers avis affichés sur la fiche. "
        "Aucune preuve d'offre alcool/bar trouvée (uniquement 'Cafés' dans Offre) — activités liées non estimées à la hausse."
    ),
    "horaires": {
        "Lundi": [("09:30", "16:30")],
        "Mardi": [("09:00", "17:00")],
        "Mercredi": [("09:00", "17:00")],
        "Jeudi": [("09:30", "16:30")],
        "Vendredi": [("09:30", "16:30")],
        "Samedi": [("09:30", "16:30")],
        "Dimanche": [("09:30", "16:30")],
    },
    "activites_priorite": {
        "Manger":               {"Matin": "P", "Midi": "P", "Après-midi": "P", "Soir": "-"},
        "Boire un café":        {"Matin": "P", "Midi": "P", "Après-midi": "P", "Soir": "-"},
        "Goûter":               {"Matin": "-", "Midi": "-", "Après-midi": "S", "Soir": "-"},
        "Boire un verre":       {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Lire":                 {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Travailler":           {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Jeux de société":      {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Jeux vidéos":          {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Écouter de la musique":{"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
        "Divertissement":       {"Matin": "-", "Midi": "-", "Après-midi": "-", "Soir": "-"},
    },
    "ambiance": {
        "Matin":       {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Midi":        {"bruit": "Fort", "luminosite": "Fort", "musique": "Modéré", "affluence": "Fort", "types": ["Sociable", "Dynamique"]},
        "Après-midi":  {"bruit": "Modéré", "luminosite": "Fort", "musique": "Faible", "affluence": "Modéré", "types": ["Sociable"]},
        "Soir":        {"bruit": "Non applicable", "luminosite": "Non applicable", "musique": "Non applicable", "affluence": "Non applicable", "types": []},
    },
    "services": ["Terrasse", "Vente à emporter", "Chiens acceptés", "Réservations acceptées"],
    "tags": ["Brunch", "Assiettes généreuses et colorées", "Pancakes moelleux et œufs bénédicte réputés"],
    "images": [
        "https://lh3.googleusercontent.com/p/AF1QipNcN7XAnK94t1wuYt2pMXGxlBDypLThmff-CZpn=w1600-h1200-k-no",
        "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSz06AMPDlYd6QkuxcKy01InUMz9z8hEY5KXnhWy08UwY6noHK4XOcjtKyavX0Wt0WC1sQ_URVWskZp7q4IqktBJt2VzRexf1Eh2KRyOzXTysyrv-hQI2lfKRAuAsacY5gBv71Kk=w1600-h1200-k-no",
        "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSyxks1ytcWUM0Cna6KuERYUgT5EP7h1BVrIW1A5pQ2o7fTeKTnQWJYY7THr3yFO4D9-wJ905Oskl5QqLuQjSnmJeFfxBr67pWrdsYMXNFGofjE8XjiiuLlNSaK1Uw0ObeEraZ-AZQfzis_u=w1600-h1200-k-no",
    ],
}

lieu_id = add_lieu(data)
print("Inserted lieu_id =", lieu_id)
import pprint
pprint.pprint(get_lieu_summary(lieu_id))
