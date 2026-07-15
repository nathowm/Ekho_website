#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Télécharge les images HD réelles de tous les lieux de la base "miroir Marseille"
directement dans Base-Lieux-Marseille/IMAGE/<nom du lieu>/, un dossier par lieu.

Pourquoi ce script existe : l'environnement sandbox où la base est gérée n'a pas
d'accès réseau sortant vers les domaines qui hébergent les images (love-spots.com,
thefork.com, lebonbon.fr, etc.). Ce script est donc prévu pour être exécuté ICI,
sur votre Mac, où l'accès internet est normal.

Usage :
    cd "~/Documents/Claude/Projects/Ekho/Base-Lieux-Marseille/IMAGE"
    python3 telecharger_images.py

Il est possible de le relancer plusieurs fois sans problème : les images déjà
présentes (même nom de fichier) ne sont pas re-téléchargées.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MANIFEST = [
  {"id": 1, "nom": "AKU", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2024/12/Aku_patisserie-japonaise_Marseille_Love-Spots_01.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2024/12/Aku_patisserie-japonaise_Marseille_Love-Spots_19.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2024/12/Aku_patisserie-japonaise_Marseille_Love-Spots_15-1.jpeg"]},
  {"id": 2, "nom": "KRM", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2026/01/KRM_Cafe-galerie_Marseille_Love-spots_11.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2026/01/KRM_Cafe-galerie_Marseille_Love-spots_01.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2026/01/KRM_Cafe-galerie_Marseille_Love-spots_08.jpeg"]},
  {"id": 3, "nom": "Bistrot Georges", "images": [
    "https://www.le-grand-pastis.com/wp-content/uploads/2026/01/Georges-une.png",
    "https://www.le-grand-pastis.com/wp-content/uploads/2026/01/Georges-deux.png",
    "https://www.le-grand-pastis.com/wp-content/uploads/2026/01/Georges-trois.png"]},
  {"id": 4, "nom": "Black Unicorn", "images": [
    "https://blackunicornmarseille.com/_assets/images/c9e9397197083dae6e5edde6d589038c.jpg"]},
  {"id": 5, "nom": "La Rêveuse", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Reveuse_librairie-a-marseille_City-guide_Love-Spots_07.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Reveuse_librairie-a-marseille_City-guide_Love-Spots_04.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Reveuse_librairie-a-marseille_City-guide_Love-Spots_11.jpg"]},
  {"id": 6, "nom": "Chaleur", "images": []},
  {"id": 7, "nom": "Sassy", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2024/04/Sassy_Bistrot-Marseille_Love-spots_04.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2024/04/Sassy_Bistrot-Marseille_Love-spots_05.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2024/04/Sassy_Bistrot-Marseille_Love-spots_06.jpeg"]},
  {"id": 8, "nom": "Mauvaise Herbe", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/06/Mauvaise-herbe_Restaurant-vegan_Marseille_Love-Spots_01.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/06/Mauvaise-herbe_Restaurant-vegan_Marseille_Love-Spots_04.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/06/Mauvaise-herbe_Restaurant-vegan_Marseille_Love-Spots_23.jpeg"]},
  {"id": 9, "nom": "Le Magnolia", "images": [
    "https://cdn.thefork.com/tf-lab/image/upload/w_1200,h_1200,c_fill,q_auto,f_jpg/restaurant/8354b82d-4da0-4fef-9f89-87c242034459/88f581b6-211e-482c-9bca-f9239b6e7372.jpg",
    "https://cdn.thefork.com/tf-lab/image/upload/w_1200,h_1200,c_fill,q_auto,f_jpg/restaurant/8354b82d-4da0-4fef-9f89-87c242034459/a78248b7-1fc4-4924-80a5-6bde5e5631b0.jpg",
    "https://cdn.thefork.com/tf-lab/image/upload/w_1200,h_1200,c_fill,q_auto,f_jpg/restaurant/8354b82d-4da0-4fef-9f89-87c242034459/41bbf2c5-9492-4d41-8bf1-2646819ef9a6.jpg"]},
  {"id": 10, "nom": "Road Social Club", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2026/03/Road-social-club_coffeeshop-boutique-fitness_Marseille_Love-spots_16.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2026/03/Road-social-club_coffeeshop-boutique-fitness_Marseille_Love-spots_23.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2026/03/Road-social-club_coffeeshop-boutique-fitness_Marseille_Love-spots_02.jpeg"]},
  {"id": 11, "nom": "Da-yé", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/07/Da-ye_coffeeshop-sandwicherie_Marseille_10.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/07/Da-ye_coffeeshop-sandwicherie_Marseille_05.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/07/Da-ye_coffeeshop-sandwicherie_Marseille_13.jpeg"]},
  {"id": 12, "nom": "Le Trois Quarts", "images": [
    "https://lh3.googleusercontent.com/p/AF1QipMLmhDt-qal3Lsbyxt66Ep8dIYKystiBYUfnGJn=w1600-h1200-k-no",
    "https://lh3.googleusercontent.com/p/AF1QipOfyPU3_7eNm5AtMqfr2IqiAUs5Pb_lU_qJW1xD=w1600-h1200-k-no",
    "https://lh3.googleusercontent.com/p/AF1QipNI7Ai4z7ubufYgHbIDiLRJsO61h_QZ8DMjhJPa=w1600-h1200-k-no"]},
  {"id": 13, "nom": "Au Jardin", "images": []},
  {"id": 14, "nom": "APT.20", "images": [
    "https://uploads.lebonbon.fr/source/2024/may/2062387/apt-20_1_2000.jpg",
    "https://uploads.lebonbon.fr/source/2024/may/2062387/apt-20_2_1200.jpg"]},
  {"id": 15, "nom": "Silk", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/09/Silk_cafe-cantine-shop-vintage_Marseille_Love-Spots_11.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/09/Silk_cafe-cantine-shop-vintage_Marseille_Love-Spots_20.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/09/Silk_cafe-cantine-shop-vintage_Marseille_Love-Spots_13.jpeg"]},
  {"id": 16, "nom": "Le 68", "images": []},
  {"id": 17, "nom": "Café Pollux", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2023/08/Pollux_Coffee-Shop_Marseille_Love-Spots_12.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2023/08/Pollux_Coffee-Shop_Marseille_Love-Spots_07.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2023/08/Pollux_Coffee-Shop_Marseille_Love-Spots_06.jpeg"]},
  {"id": 18, "nom": "Pulse Café", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/09/Pulse-Cafe-Longchamp_Cantine-Boutique-Studio-Yoga_Marseille_Love-Spots_01.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/09/Pulse-Cafe-Longchamp_Cantine-Boutique-Studio-Yoga_Marseille_Love-Spots_05.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/09/Pulse-Cafe-Longchamp_Cantine-Boutique-Studio-Yoga_Marseille_Love-Spots_04.jpeg"]},
  {"id": 19, "nom": "Café LaMuse", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2021/08/Cafe-La-Muse_Cafe_Marseille_City-guide_Love-Spots_02.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/08/Cafe-La-Muse_Cafe_Marseille_City-guide_Love-Spots_00.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/08/Cafe-La-Muse_Cafe_Marseille_City-guide_Love-Spots_09.jpg"]},
  {"id": 20, "nom": "Le Poulpe (Saint-Victor)", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Bar-a-tapas_Marseille_Le-Poulpe-Saint-Victor_Love-spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Bar-a-tapas_Marseille_Le-Poulpe-Saint-Victor_Love-spots_08.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Bar-a-tapas_Marseille_Le-Poulpe-Saint-Victor_Love-spots_03.jpg"]},
  {"id": 21, "nom": "Mat'cha", "images": [
    "https://itin-dev.wanderlogstatic.com/freeImageSmall/1tDrwuJaegajebr6HoRA966wYo8osyZ2"]},
  {"id": 22, "nom": "Polpette", "images": [
    "https://toutma.fr/wp-content/uploads/2026/05/polpette-marseille.jpg",
    "https://toutma.fr/wp-content/uploads/2026/05/polpette-marseille-restaurant-768x1024.jpg",
    "https://toutma.fr/wp-content/uploads/2026/05/polpette-restaurant-576x1024.jpg"]},
  {"id": 23, "nom": "Black Bird Coffee", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Coffee-shop_Marseille_Black-Bird-Coffee_Love-spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Coffee-shop_Marseille_Black-Bird-Coffee_Love-spots_14.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2019/04/Coffee-shop_Marseille_Black-Bird-Coffee_Love-spots_13.jpg"]},
  {"id": 24, "nom": "Lala Café", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Lala-cafe_cafe-cantine-shop_Marseille_Love-Spots_09.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Lala-cafe_cafe-cantine-shop_Marseille_Love-Spots_01.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Lala-cafe_cafe-cantine-shop_Marseille_Love-Spots_16.jpeg"]},
  {"id": 25, "nom": "Risette", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/06/Risette_coffeshop-daily_Marseille_Love-Spots_21.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/06/Risette_coffeshop-daily_Marseille_Love-Spots_19.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/06/Risette_coffeshop-daily_Marseille_Love-Spots_16.jpeg"]},
  {"id": 26, "nom": "La Fiancée", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop-Marseille_la-Fiancee_Love-spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop-Marseille_la-Fiancee_Love-spots_03.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop-Marseille_la-Fiancee_Love-spots_04.jpg"]},
  {"id": 27, "nom": "Fyne Urban Kahwa", "images": [
    "https://www.fyne-urban-kahwa-restaurant-marseille.fr/media/cache/resolve/l600lq/websites/5b397cbda1ce28634ab499eedeee6fbf/img/Frame%2053_20240108155925.jpg",
    "https://www.fyne-urban-kahwa-restaurant-marseille.fr/media/cache/resolve/l600lq/websites/5b397cbda1ce28634ab499eedeee6fbf/img/Frame%2050_20240108162211.jpg",
    "https://www.fyne-urban-kahwa-restaurant-marseille.fr/media/cache/resolve/l600lq/websites/5b397cbda1ce28634ab499eedeee6fbf/img/Frame%2051_20240108155920.jpg"]},
  {"id": 28, "nom": "Maison Bahja", "images": [
    "https://api.cloudly.space/resize/cropratio/1920/1080/75/aHR0cHM6Ly9zdGF0aWMuYXBpZGFlLXRvdXJpc21lLmNvbS9maWxlc3RvcmUvb2JqZXRzLXRvdXJpc3RpcXVlcy9pbWFnZXMvMTgzLzMxLzM3MzYzNjM5LmpwZw==/image.webp",
    "https://api.cloudly.space/resize/cropratio/1920/1080/75/aHR0cHM6Ly9zdGF0aWMuYXBpZGFlLXRvdXJpc21lLmNvbS9maWxlc3RvcmUvb2JqZXRzLXRvdXJpc3RpcXVlcy9pbWFnZXMvMTg1LzMxLzM3MzYzNjQxLmpwZw==/image.webp"]},
  {"id": 29, "nom": "Voilà Vé", "images": [
    "https://madeinmarseille.net/actualites-marseille/2019/11/vin-camas-chave.jpg",
    "https://madeinmarseille.net/actualites-marseille/2019/11/tapas-vin.jpg",
    "https://madeinmarseille.net/actualites-marseille/2019/11/chave-camas.jpg"]},
  {"id": 30, "nom": "Pétrin Couchette", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2022/05/Petrin-Couchett_Boulangerie-et-Cafe-Marseille_City-guide-Love-Spots_03.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2022/05/Petrin-Couchett_Boulangerie-et-Cafe-Marseille_City-guide-Love-Spots_02.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2022/04/Petrin-couchette_Marseille_City-Guide_Love-Spots_07.jpg"]},
  {"id": 32, "nom": "Mon Gâté", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2024/03/Mon-Gate_Cafe_Choux_Marseille_Love-spots_01.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2024/03/Mon-Gate_Cafe_Choux_Marseille_Love-spots_03.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2024/03/Mon-Gate_Cafe_Choux_Marseille_Love-spots_11.jpeg"]},
  {"id": 33, "nom": "Josie", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/10/Josie_coffee-shop_Marseille_Love-Spots_15.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/10/Josie_coffee-shop_Marseille_Love-Spots_05.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/10/Josie_coffee-shop_Marseille_Love-Spots_16.jpeg"]},
  {"id": 34, "nom": "Brûlerie Möka", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2019/09/Brulerie-Moka_Torrefaction-Marseille_Love-Spots_08.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2019/09/Brulerie-Moka_Torrefaction-Marseille_Love-Spots_05.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2019/09/Brulerie-Moka_Torrefaction-Marseille_Love-Spots_04.jpg"]},
  {"id": 35, "nom": "Le Petit Café", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2023/02/Le-Petit-Cafe_Marseille_City-Guide_Love-Spots_03.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2023/02/Le-Petit-Cafe_Marseille_City-Guide_Love-Spots_02.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2023/02/Le-Petit-Cafe_Marseille_City-Guide_Love-Spots_05.jpg"]},
  {"id": 36, "nom": "Mañana", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2026/02/manana_cafe-de-quartier_marseille_love-spots_05.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2026/02/manana_cafe-de-quartier_marseille_love-spots_19-1.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2026/02/manana_cafe-de-quartier_marseille_love-spots_16.jpeg"]},
  {"id": 39, "nom": "Maurice", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/04/Maurice_bistrot-bar-cantine_Marseille_Love-spots_09.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/04/Maurice_bistrot-bar-cantine_Marseille_Love-spots_07.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/04/Maurice_bistrot-bar-cantine_Marseille_Love-spots_16.jpeg"]},
  {"id": 40, "nom": "Les Babines de Mars", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/05/Les-Babines-de-Mars_Bistrot-Marseille_Love-spots_12.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/05/Les-Babines-de-Mars_Bistrot-Marseille_Love-spots_13.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/05/Les-Babines-de-Mars_Bistrot-Marseille_Love-spots_07.jpeg"]},
  {"id": 41, "nom": "Yuzu Record Bar", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Yuzu-record-bar_Bar-audiophile_Marseille_Love-Spots_10.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Yuzu-record-bar_Bar-audiophile_Marseille_Love-Spots_13.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Yuzu-record-bar_Bar-audiophile_Marseille_Love-Spots_05.jpeg"]},
  {"id": 42, "nom": "Grand Écart", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Grand-ecart_Social-sport-club_marseille_Love-spots_04.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Grand-ecart_Social-sport-club_marseille_Love-spots_05.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2025/12/Grand-ecart_Social-sport-club_marseille_Love-spots_11.jpeg"]},
  {"id": 43, "nom": "7VB Café", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop_Marseille_7VB_Love-spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop_Marseille_7VB_Love-spots_02.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2018/11/Coffee-shop_Marseille_7VB_Love-spots_11.jpg"]},
  {"id": 44, "nom": "Chez Moe", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2024/08/Chez_Moe_cantine_coffee_shop_love_spots_13-scaled.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2024/08/Chez_Moe_cantine_coffee_shop_love_spots_05-scaled.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2024/08/Chez_Moe_cantine_coffee_shop_love_spots_01-scaled.jpeg"]},
  {"id": 45, "nom": "Maison Nosh", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2026/03/maison-nosh_brunch_marseille_love-spots_05.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2026/03/maison-nosh_brunch_marseille_love-spots_13.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2026/03/maison-nosh_brunch_marseille_love-spots_10.jpg"]},
  {"id": 47, "nom": "La Caravelle", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2013/12/bar_marseille_lovespots_la-caravelle_01.jpg"]},
  {"id": 48, "nom": "John Silver", "images": [
    "https://toutma.fr/wp-content/uploads/2026/01/John-Silver_devanture_Cedric-Villetorte-©laurettecie-786x1024.jpeg",
    "https://toutma.fr/wp-content/uploads/2026/01/John-Silver_salle_3-©laurettecie-683x1024.jpeg",
    "https://toutma.fr/wp-content/uploads/2026/01/John-Silver_recette_2©laurettecie-scaled.jpeg"]},
  {"id": 49, "nom": "Ivresse", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2022/11/Ivresse_Cave-et-Bar-a-vins-nature_Marseille_City-guide_Love-spots_03.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2022/11/Ivresse_Cave-et-Bar-a-vins-nature_Marseille_City-guide_Love-spots_05.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2022/11/Ivresse_Cave-et-Bar-a-vins-nature_Marseille_City-guide_Love-spots_08.jpeg"]},
  {"id": 52, "nom": "Le Molotov", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2012/08/salle-de-concerts-marseille-molotov-lovespots-1.jpg",
    "http://lemolotov.com/wp-content/uploads/2019/08/lemolotovmarseille.jpg"]},
  {"id": 53, "nom": "Mercato by Winesucker", "images": [
    "https://lh3.googleusercontent.com/places/ANJU3DuWEXHuqUrsbKk5i9ZROfxXjdMT3c2Rxrm6DGaf_HTzDTDjQp72ALG7nb4dT_WmXWKM-AUhM3ANcCHiV3X9jyuaaIk7XfvJVYw=s1600-w640",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSzpkArPba_FknncUdsRR-AvoL6ixUuxPEP9zZ_3W7oa_dRxPbfLzE1mOP2A0lrKkY1NQa03DagAu0an7JgwQmwHN5Sq690tdojGSriIPywfZXbsxUo7OgfHeMcFXPilPXz7V5bB=w1600-h1200-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSxCIecIaJGAstbs0ke5d1ooNLQyi2sUUEK5SF4PJeaGcpxsQo1epZNjBaw5YgYp3VyBZITRqXkcshyHdwRK-Cgtc-F1vIuycPE7ztqbtNd9zvJOak8KY3gdz44KQ_0DNm-Dm1o=w1600-h1200-k-no"]},
  {"id": 57, "nom": "Café de l'Abbaye", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2010/10/cafe-de-l-abbaye_love-spots-marseille_01.jpg"]},
  {"id": 58, "nom": "Les Succulentes", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2018/02/Cafe-cactus_Marseille_Les-Succulentes_Love-Spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2018/02/Cafe-cactus_Marseille_Les-Succulentes_Love-Spots_05.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2018/02/Cafe-cactus_Marseille_Les-Succulentes_Love-Spots_02.jpg"]},
  {"id": 59, "nom": "Deïa Coffee & Kitchen", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2024/06/Deia_Brunch_Healthy_Restaurant_-_Marseille_Love_spots_17.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2024/06/Deia_Brunch_Healthy_Restaurant_-_Marseille_Love_spots_09-scaled.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2024/06/Deia_Brunch_Healthy_Restaurant_-_Marseille_Love_spots_07-scaled.jpeg"]},
  {"id": 60, "nom": "Café de la Consigne", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2026/03/Le-Cafe-de-la-Consigne_Bar-et-cantine_Marseille_01.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2026/03/Le-Cafe-de-la-Consigne_Bar-et-cantine_Marseille_02.jpeg",
    "https://marseille.love-spots.com/wp-content/uploads/2026/03/Le-Cafe-de-la-Consigne_Bar-et-cantine_Marseille_03.jpeg"]},
  {"id": 61, "nom": "Baghera Café", "images": [
    "https://lh3.googleusercontent.com/p/AF1QipNcN7XAnK94t1wuYt2pMXGxlBDypLThmff-CZpn=w1600-h1200-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSz06AMPDlYd6QkuxcKy01InUMz9z8hEY5KXnhWy08UwY6noHK4XOcjtKyavX0Wt0WC1sQ_URVWskZp7q4IqktBJt2VzRexf1Eh2KRyOzXTysyrv-hQI2lfKRAuAsacY5gBv71Kk=w1600-h1200-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSyxks1ytcWUM0Cna6KuERYUgT5EP7h1BVrIW1A5pQ2o7fTeKTnQWJYY7THr3yFO4D9-wJ905Oskl5QqLuQjSnmJeFfxBr67pWrdsYMXNFGofjE8XjiiuLlNSaK1Uw0ObeEraZ-AZQfzis_u=w1600-h1200-k-no"]},
  {"id": 63, "nom": "Au Comptoir du Livre", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2022/12/Au-comptoir-du-livre_cafe-librairie-Marseille_City-guide_Love-Spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2022/12/Au-comptoir-du-livre_cafe-librairie-Marseille_City-guide_Love-Spots_35.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2022/12/Au-comptoir-du-livre_cafe-librairie-Marseille_City-guide_Love-Spots_25.jpg"]},
  {"id": 64, "nom": "Ben Mouture", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2023/09/Ben-Mouture_Marseille_City-Guide_Love-Spots_02.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2023/09/Ben-Mouture_Marseille_City-Guide_Love-Spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2023/09/Ben-Mouture_Marseille_City-Guide_Love-Spots_03.jpg"]},
  {"id": 65, "nom": "La Tisserie", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Tisserie_Torrefaction_Marseille_City-Guide_Love-Spots_01.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Tisserie_Torrefaction_Marseille_City-Guide_Love-Spots_10-1.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/12/La-Tisserie_Torrefaction_Marseille_City-Guide_Love-Spots_08-2.jpg"]},
  {"id": 66, "nom": "Maison des Nines", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2021/07/Maison-des-Nines_Boutique-Cantine_Table-d-hote_Noailles_Marseille_City-Guide_Love-Spots_11.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/07/Maison-des-Nines_Boutique-Cantine_Table-d-hote_Noailles_Marseille_City-Guide_Love-Spots_04.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/07/Maison-des-Nines_Boutique-Cantine_Table-d-hote_Noailles_Marseille_City-Guide_Love-Spots_05.jpg"]},
  {"id": 67, "nom": "Café Lauca « La Boutchica »", "images": [
    "https://marseille.love-spots.com/wp-content/uploads/2021/11/Cafe-Lauca_La-Boutchica-_coffee-shop_marseille_City-guide_Love-Spots_09.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/11/Cafe-Lauca_La-Boutchica-_coffee-shop_marseille_City-guide_Love-Spots_06.jpg",
    "https://marseille.love-spots.com/wp-content/uploads/2021/11/Cafe-Lauca_La-Boutchica-_coffee-shop_marseille_City-guide_Love-Spots_02.jpg"]},
]


def sanitize(name):
    name = name.replace("/", "-").replace(":", "-").replace("*", "").replace("?", "")
    name = name.replace('"', "'").replace("<", "").replace(">", "").replace("|", "-")
    return name.strip()


def filename_from_url(url, index):
    base = url.split("?")[0].rstrip("/").split("/")[-1]
    if not base or "." not in base:
        base = f"image_{index:02d}.jpg"
    # sécuriser aussi le nom de fichier lui-même
    base = re.sub(r"[^A-Za-z0-9._-]", "_", base)
    return base


def main():
    total_ok = 0
    total_skip = 0
    total_fail = 0
    failures = []

    for lieu in MANIFEST:
        nom = lieu["nom"]
        folder = os.path.join(BASE_DIR, sanitize(nom))
        os.makedirs(folder, exist_ok=True)

        if not lieu["images"]:
            print(f"[{nom}] aucune image disponible pour l'instant (source non trouvée).")
            continue

        for i, url in enumerate(lieu["images"], start=1):
            fname = filename_from_url(url, i)
            dest = os.path.join(folder, fname)
            if os.path.exists(dest) and os.path.getsize(dest) > 0:
                total_skip += 1
                continue
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=20) as resp, open(dest, "wb") as f:
                    f.write(resp.read())
                size_kb = os.path.getsize(dest) / 1024
                print(f"[{nom}] OK  -> {fname} ({size_kb:.0f} Ko)")
                total_ok += 1
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
                print(f"[{nom}] ECHEC -> {fname} : {e}")
                failures.append((nom, url, str(e)))
                total_fail += 1

    print("\n--- Résumé ---")
    print(f"Téléchargées : {total_ok}")
    print(f"Déjà présentes (ignorées) : {total_skip}")
    print(f"Échecs : {total_fail}")
    if failures:
        print("\nDétail des échecs :")
        for nom, url, err in failures:
            print(f" - {nom}: {url}\n   -> {err}")

    print("\nLieux sans image trouvée (recherche à poursuivre) : "
          + ", ".join(l["nom"] for l in MANIFEST if not l["images"]))


if __name__ == "__main__":
    main()
