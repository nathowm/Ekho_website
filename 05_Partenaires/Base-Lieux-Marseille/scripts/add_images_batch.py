import sqlite3

conn = sqlite3.connect('lieux_mirror.db')
cur = conn.cursor()

IMAGES = {
    1: [  # AKU - garder l'existante _01, ajouter 2
        "https://marseille.love-spots.com/wp-content/uploads/2024/12/Aku_patisserie-japonaise_Marseille_Love-Spots_01.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2024/12/Aku_patisserie-japonaise_Marseille_Love-Spots_19.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2024/12/Aku_patisserie-japonaise_Marseille_Love-Spots_15-1.jpeg",
    ],
    2: [  # KRM
        "https://marseille.love-spots.com/wp-content/uploads/2026/01/KRM_Cafe-galerie_Marseille_Love-spots_11.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/01/KRM_Cafe-galerie_Marseille_Love-spots_01.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/01/KRM_Cafe-galerie_Marseille_Love-spots_08.jpeg",
    ],
    4: [  # Black Unicorn - 1 seule trouvée malgré recherche croisée (site officiel, FB, Insta, Yelp bloqués)
        "https://blackunicornmarseille.com/_assets/images/c9e9397197083dae6e5edde6d589038c.jpg",
    ],
    5: [  # La Rêveuse
        "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Reveuse_librairie-a-marseille_City-guide_Love-Spots_07.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Reveuse_librairie-a-marseille_City-guide_Love-Spots_04.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Reveuse_librairie-a-marseille_City-guide_Love-Spots_11.jpg",
    ],
    7: [  # Sassy
        "https://marseille.love-spots.com/wp-content/uploads/2024/04/Sassy_Bistrot-Marseille_Love-spots_04.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2024/04/Sassy_Bistrot-Marseille_Love-spots_05.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2024/04/Sassy_Bistrot-Marseille_Love-spots_06.jpeg",
    ],
    8: [  # Mauvaise Herbe
        "https://marseille.love-spots.com/wp-content/uploads/2025/06/Mauvaise-herbe_Restaurant-vegan_Marseille_Love-Spots_01.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/06/Mauvaise-herbe_Restaurant-vegan_Marseille_Love-Spots_04.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/06/Mauvaise-herbe_Restaurant-vegan_Marseille_Love-Spots_23.jpeg",
    ],
    9: [  # Le Magnolia (TheFork)
        "https://cdn.thefork.com/tf-lab/image/upload/w_1200,h_1200,c_fill,q_auto,f_jpg/restaurant/8354b82d-4da0-4fef-9f89-87c242034459/88f581b6-211e-482c-9bca-f9239b6e7372.jpg",
        "https://cdn.thefork.com/tf-lab/image/upload/w_1200,h_1200,c_fill,q_auto,f_jpg/restaurant/8354b82d-4da0-4fef-9f89-87c242034459/a78248b7-1fc4-4924-80a5-6bde5e5631b0.jpg",
        "https://cdn.thefork.com/tf-lab/image/upload/w_1200,h_1200,c_fill,q_auto,f_jpg/restaurant/8354b82d-4da0-4fef-9f89-87c242034459/41bbf2c5-9492-4d41-8bf1-2646819ef9a6.jpg",
    ],
    10: [  # Road Social Club
        "https://marseille.love-spots.com/wp-content/uploads/2026/03/Road-social-club_coffeeshop-boutique-fitness_Marseille_Love-spots_16.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/03/Road-social-club_coffeeshop-boutique-fitness_Marseille_Love-spots_23.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2026/03/Road-social-club_coffeeshop-boutique-fitness_Marseille_Love-spots_02.jpeg",
    ],
    14: [  # APT.20 - seulement 2 trouvées (Le Bonbon), pas de 3e source fiable identifiée
        "https://uploads.lebonbon.fr/source/2024/may/2062387/apt-20_1_2000.jpg",
        "https://uploads.lebonbon.fr/source/2024/may/2062387/apt-20_2_1200.jpg",
    ],
    15: [  # Silk
        "https://marseille.love-spots.com/wp-content/uploads/2025/09/Silk_cafe-cantine-shop-vintage_Marseille_Love-Spots_11.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/09/Silk_cafe-cantine-shop-vintage_Marseille_Love-Spots_20.jpeg",
        "https://marseille.love-spots.com/wp-content/uploads/2025/09/Silk_cafe-cantine-shop-vintage_Marseille_Love-Spots_13.jpeg",
    ],
    19: [  # Café LaMuse
        "https://marseille.love-spots.com/wp-content/uploads/2021/08/Cafe-La-Muse_Cafe_Marseille_City-guide_Love-Spots_02.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2021/08/Cafe-La-Muse_Cafe_Marseille_City-guide_Love-Spots_00.jpg",
        "https://marseille.love-spots.com/wp-content/uploads/2021/08/Cafe-La-Muse_Cafe_Marseille_City-guide_Love-Spots_09.jpg",
    ],
    21: [  # Mat'cha - 1 seule trouvée (Wanderlog), aucune autre source fiable avec image directe
        "https://itin-dev.wanderlogstatic.com/freeImageSmall/1tDrwuJaegajebr6HoRA966wYo8osyZ2",
    ],
    22: [  # Polpette (Le Grand Pastis)
        "https://www.le-grand-pastis.com/wp-content/uploads/2026/04/Polpette-huit.png",
        "https://www.le-grand-pastis.com/wp-content/uploads/2026/04/Polpette-une.png",
        "https://www.le-grand-pastis.com/wp-content/uploads/2026/04/Polpette-trois.png",
    ],
    27: [  # Fyne Urban Kahwa (site officiel)
        "https://www.fyne-urban-kahwa-restaurant-marseille.fr/media/cache/resolve/l600lq/websites/5b397cbda1ce28634ab499eedeee6fbf/img/Frame%2053_20240108155925.jpg",
        "https://www.fyne-urban-kahwa-restaurant-marseille.fr/media/cache/resolve/l600lq/websites/5b397cbda1ce28634ab499eedeee6fbf/img/Frame%2050_20240108162211.jpg",
        "https://www.fyne-urban-kahwa-restaurant-marseille.fr/media/cache/resolve/l600lq/websites/5b397cbda1ce28634ab499eedeee6fbf/img/Frame%2051_20240108155920.jpg",
    ],
    28: [  # Maison Bahja - 2 trouvées (office de tourisme PACA), pas de 3e confirmee
        "https://api.cloudly.space/resize/cropratio/1920/1080/75/aHR0cHM6Ly9zdGF0aWMuYXBpZGFlLXRvdXJpc21lLmNvbS9maWxlc3RvcmUvb2JqZXRzLXRvdXJpc3RpcXVlcy9pbWFnZXMvMTgzLzMxLzM3MzYzNjM5LmpwZw==/image.webp",
        "https://api.cloudly.space/resize/cropratio/1920/1080/75/aHR0cHM6Ly9zdGF0aWMuYXBpZGFlLXRvdXJpc21lLmNvbS9maWxlc3RvcmUvb2JqZXRzLXRvdXJpc3RpcXVlcy9pbWFnZXMvMTg1LzMxLzM3MzYzNjQxLmpwZw==/image.webp",
    ],
    29: [  # Voila Vé (Made in Marseille)
        "https://madeinmarseille.net/actualites-marseille/2019/11/vin-camas-chave.jpg",
        "https://madeinmarseille.net/actualites-marseille/2019/11/tapas-vin.jpg",
        "https://madeinmarseille.net/actualites-marseille/2019/11/chave-camas.jpg",
    ],
}

for lieu_id, urls in IMAGES.items():
    cur.execute("DELETE FROM images WHERE lieu_id=?", (lieu_id,))
    for i, url in enumerate(urls, start=1):
        cur.execute("INSERT INTO images (lieu_id, url, ordre) VALUES (?,?,?)", (lieu_id, url, i))
    print(lieu_id, "->", len(urls), "image(s)")

conn.commit()

# Rapport final
print("\n--- Etat final ---")
rows = cur.execute("""
    SELECT l.id, l.nom, COUNT(i.id) FROM lieux l LEFT JOIN images i ON i.lieu_id=l.id
    GROUP BY l.id ORDER BY l.id
""").fetchall()
for lid, nom, n in rows:
    marker = " <-- toujours < 3" if n < 3 else ""
    print(lid, nom, n, marker)
conn.close()
