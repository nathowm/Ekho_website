import sqlite3
from pathlib import Path

DB_PATH = Path("lieux_mirror.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

def set_images(lid, urls):
    cur.execute("DELETE FROM images WHERE lieu_id=?", (lid,))
    for i, u in enumerate(urls, start=1):
        cur.execute("INSERT INTO images (lieu_id, url, ordre) VALUES (?,?,?)", (lid, u, i))

def set_horaires(lid, schedule):
    # schedule: dict jour -> list of (debut,fin) or None if fermé
    cur.execute("DELETE FROM horaires_tranches WHERE lieu_id=?", (lid,))
    for jour, tranches in schedule.items():
        if not tranches:
            cur.execute("INSERT INTO horaires_tranches (lieu_id, jour, ferme) VALUES (?,?,1)", (lid, jour))
        else:
            for d, f in tranches:
                cur.execute(
                    "INSERT INTO horaires_tranches (lieu_id, jour, ferme, heure_debut, heure_fin) VALUES (?,?,0,?,?)",
                    (lid, jour, d, f))

def update_lieu_fields(lid, **fields):
    set_clause = ", ".join(f"{k}=?" for k in fields)
    cur.execute(f"UPDATE lieux SET {set_clause}, updated_at=datetime('now') WHERE id=?",
                list(fields.values()) + [lid])

# ---------- 3: Georges ----------
update_lieu_fields(3,
    telephone_public="09 84 30 53 28",
    source_donnees=("Recherche web 13/07/2026 : love-spots.com (article du 02/04/2015 - ancien, "
                     "adresse 115 Bd Chave, indique 13004 alors que le reste du cluster Bd Chave "
                     "utilisé ici est en 13005 ; horaires anciens mar-sam 8h-15h, non fiables car "
                     "obsolètes) + sources plus récentes (mar-sam 8h-22h30, conservées comme réf. "
                     "principale). Tél. et image tirés de love-spots. A reconfirmer sur place."))
set_images(3, [
    "https://marseille.love-spots.com/wp-content/uploads/2015/04/love-spots_georges_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2015/04/love-spots_georges_02.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2015/04/love-spots_georges_03.jpg",
])

# ---------- 11: Da-yé ----------
set_images(11, [
    "https://marseille.love-spots.com/wp-content/uploads/2025/07/Da-ye_coffeeshop-sandwicherie_Marseille_10.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/07/Da-ye_coffeeshop-sandwicherie_Marseille_05.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/07/Da-ye_coffeeshop-sandwicherie_Marseille_13.jpeg",
])

# ---------- 17: Café Pollux ----------
set_images(17, [
    "https://marseille.love-spots.com/wp-content/uploads/2023/08/Pollux_Coffee-Shop_Marseille_Love-Spots_12.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2023/08/Pollux_Coffee-Shop_Marseille_Love-Spots_07.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2023/08/Pollux_Coffee-Shop_Marseille_Love-Spots_06.jpeg",
])

# ---------- 18: Pulse Café (correction horaires: lundi ouvert 11h-15h30, pas fermé) ----------
set_horaires(18, {
    "Lundi": [("11:00", "15:30")],
    "Mardi": [("09:00", "18:00")],
    "Mercredi": [("09:00", "18:00")],
    "Jeudi": [("09:00", "18:00")],
    "Vendredi": [("09:00", "18:00")],
    "Samedi": [("09:00", "15:00")],
    "Dimanche": None,
})
update_lieu_fields(18, site_web="http://pulse-cafe.com/",
    source_donnees=("Recherche web 13/07/2026 : love-spots.com (06/10/2025). Correction : "
                     "lundi ouvert 11h-15h30 (et non fermé comme précédemment enregistré). "
                     "Samedi 9h-15h (et non 9h-18h)."))
set_images(18, [
    "https://marseille.love-spots.com/wp-content/uploads/2025/09/Pulse-Cafe-Longchamp_Cantine-Boutique-Studio-Yoga_Marseille_Love-Spots_01.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/09/Pulse-Cafe-Longchamp_Cantine-Boutique-Studio-Yoga_Marseille_Love-Spots_05.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/09/Pulse-Cafe-Longchamp_Cantine-Boutique-Studio-Yoga_Marseille_Love-Spots_04.jpeg",
])
# ambiance had been mechanically filled already assuming old (wrong) hours; matin/apres-midi profiles remain fine
# but re-add moment coverage check: Lundi ouvert 11-15h30 only affects overall week union, Midi/Apres-midi already open via mardi-samedi

# ---------- 20: Le Poulpe Saint-Victor ----------
set_images(20, [
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Bar-a-tapas_Marseille_Le-Poulpe-Saint-Victor_Love-spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Bar-a-tapas_Marseille_Le-Poulpe-Saint-Victor_Love-spots_08.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Bar-a-tapas_Marseille_Le-Poulpe-Saint-Victor_Love-spots_03.jpg",
])

# ---------- 23: Black Bird Coffee (correction horaires) ----------
set_horaires(23, {
    "Lundi": [("07:00", "19:00")],
    "Mardi": [("07:00", "19:00")],
    "Mercredi": [("07:00", "19:00")],
    "Jeudi": [("07:00", "19:00")],
    "Vendredi": [("07:00", "19:00")],
    "Samedi": [("08:30", "19:00")],
    "Dimanche": [("08:30", "19:00")],
})
update_lieu_fields(23, telephone_public="06 64 00 19 31",
    source_donnees=("Recherche web 13/07/2026 : love-spots.com (29/04/2019). Correction horaires : "
                     "lun-ven 7h-19h, sam-dim 8h30-19h (au lieu du planning irrégulier précédemment "
                     "enregistré, probablement erroné)."))
set_images(23, [
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Coffee-shop_Marseille_Black-Bird-Coffee_Love-spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Coffee-shop_Marseille_Black-Bird-Coffee_Love-spots_14.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Coffee-shop_Marseille_Black-Bird-Coffee_Love-spots_13.jpg",
])

# ---------- 24: Lala Café ----------
set_images(24, [
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Lala-cafe_cafe-cantine-shop_Marseille_Love-Spots_09.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Lala-cafe_cafe-cantine-shop_Marseille_Love-Spots_01.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Lala-cafe_cafe-cantine-shop_Marseille_Love-Spots_16.jpeg",
])

# ---------- 25: Risette ----------
set_images(25, [
    "https://marseille.love-spots.com/wp-content/uploads/2025/06/Risette_coffeshop-daily_Marseille_Love-Spots_21.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/06/Risette_coffeshop-daily_Marseille_Love-Spots_19.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/06/Risette_coffeshop-daily_Marseille_Love-Spots_16.jpeg",
])

# ---------- 26: La Fiancée (correction téléphone/horaires) ----------
set_horaires(26, {
    "Lundi": [("09:30", "17:30")],
    "Mardi": [("09:30", "17:30")],
    "Mercredi": [("09:30", "17:30")],
    "Jeudi": [("09:30", "17:30")],
    "Vendredi": [("09:30", "17:30")],
    "Samedi": [("10:00", "17:30")],
    "Dimanche": [("11:30", "17:30")],
})
update_lieu_fields(26, telephone_public="09 83 46 70 56", site_web="http://cafelafiancee.com",
    source_donnees=("Recherche web 13/07/2026 : love-spots.com (15/11/2018). Correction : "
                     "téléphone 09 83 46 70 56 (absent auparavant), horaires lun-ven 9h30-17h30, "
                     "sam 10h-17h30, dim 11h30-17h30 (précédemment enregistrés différemment)."))
set_images(26, [
    "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop-Marseille_la-Fiancee_Love-spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop-Marseille_la-Fiancee_Love-spots_03.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop-Marseille_la-Fiancee_Love-spots_04.jpg",
])

# ---------- 30: Pétrin Couchette (téléphone + horaires + site) ----------
set_horaires(30, {
    "Lundi": None,
    "Mardi": [("08:00", "18:00")],
    "Mercredi": [("08:00", "18:00")],
    "Jeudi": [("08:00", "18:00")],
    "Vendredi": [("08:00", "18:00")],
    "Samedi": [("08:00", "18:00")],
    "Dimanche": [("08:00", "18:00")],
})
update_lieu_fields(30, telephone_public="06 45 32 53 27", site_web="http://www.petrincouchette.com",
    source_donnees=("Recherche web 13/07/2026 : love-spots.com (13/05/2022). Ajout téléphone "
                     "06 45 32 53 27 et site web ; correction horaires 8h-18h (au lieu de 9h-19h)."))
set_images(30, [
    "https://marseille.love-spots.com/wp-content/uploads/2022/05/Petrin-Couchett_Boulangerie-et-Cafe-Marseille_City-guide-Love-Spots_03.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2022/05/Petrin-Couchett_Boulangerie-et-Cafe-Marseille_City-guide-Love-Spots_02.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2022/04/Petrin-couchette_Marseille_City-Guide_Love-Spots_07.jpg",
])

# ---------- 31: Vorace (téléphone + site + images ; horaires déjà correctes) ----------
update_lieu_fields(31, telephone_public="04 91 92 06 74",
    source_donnees=("Recherche web 13/07/2026 : love-spots.com (07/09/2021). Ajout téléphone "
                     "04 91 92 06 74. Horaires (lun-sam 8h-23h) confirmées conformes à la fiche existante."))
set_images(31, [
    "https://marseille.love-spots.com/wp-content/uploads/2021/09/Vorace_Bistrot_Marseille_City-Guide_Love-Spots_05.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/09/Vorace_Bistrot_Marseille_City-Guide_Love-Spots_02.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/09/Vorace_Bistrot_Marseille_City-Guide_Love-Spots_10.jpg",
])

conn.commit()
conn.close()
print("Corrections applied.")
