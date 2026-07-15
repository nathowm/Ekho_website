"""
Helper réutilisable pour ajouter / mettre à jour une fiche "lieu" dans la
base miroir locale (lieux_mirror.db), à partir d'un simple dictionnaire
Python. Sert de brique commune à toute complétion future de la base.

Exemple minimal :
    from lieu_helper import add_lieu
    add_lieu({
        "nom": "Mon Lieu",
        "types": ["Café"],
        "adresse": "1 rue Exemple, 13001 Marseille",
    })

Champs disponibles dans le dict (tous optionnels sauf "nom") :
    nom, partenaire, lieu_actif, types (liste), code_postal, arrondissement,
    quartier, adresse, latitude, longitude, lien_google_maps, note_google,
    nombre_avis_google, site_web, telephone_public, niveau_engagement,
    gamme_prix, cadre, source_donnees,
    horaires: {"Lundi": [("08:00","23:00"), ...] ou None si fermé, ...},
    phrases_accroche: {"Matin": "...", "Midi": "...", "Après-midi": "...", "Soir": "..."},
    contact: {"nom":..., "prenom":..., "email":..., "telephone_portable":...},
    activites_priorite: {"Boire un café": {"Matin": "P", "Midi": "S", ...}, ...},
    ambiance: {"Matin": {"bruit":..., "luminosite":..., "musique":..., "affluence":...,
                          "types": ["Calme", "Sociable"]}, ...},
    services: ["Wifi", "Terrasse", ...],
    tags: ["Cosy", "Café Spécialisé", ...],
    images: ["url1", "url2", ...]  (la 1ère = couverture)
"""
import sqlite3
from pathlib import Path

DB_PATH = Path('/tmp/lieux_db/lieux_mirror.db')


def _get_or_create_id(cur, table, nom):
    cur.execute(f"SELECT id FROM {table} WHERE nom = ?", (nom,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(f"INSERT INTO {table} (nom) VALUES (?)", (nom,))
    return cur.lastrowid


def add_lieu(data: dict, lieu_id: int | None = None) -> int:
    """Insère un nouveau lieu (ou met à jour lieu_id existant) et toutes ses
    données liées. Retourne l'id du lieu."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    fields = {
        "nom": data.get("nom"),
        "partenaire": int(bool(data.get("partenaire", False))),
        "lieu_actif": int(bool(data.get("lieu_actif", False))),
        "code_postal": data.get("code_postal"),
        "arrondissement": data.get("arrondissement"),
        "quartier": data.get("quartier"),
        "adresse": data.get("adresse"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "lien_google_maps": data.get("lien_google_maps"),
        "note_google": data.get("note_google"),
        "nombre_avis_google": data.get("nombre_avis_google"),
        "site_web": data.get("site_web"),
        "telephone_public": data.get("telephone_public"),
        "niveau_engagement": data.get("niveau_engagement"),
        "gamme_prix": data.get("gamme_prix"),
        "cadre": data.get("cadre"),
        "source_donnees": data.get("source_donnees"),
    }

    if lieu_id is None:
        cols = ", ".join(fields.keys())
        placeholders = ", ".join("?" for _ in fields)
        cur.execute(f"INSERT INTO lieux ({cols}) VALUES ({placeholders})", list(fields.values()))
        lieu_id = cur.lastrowid
    else:
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        cur.execute(
            f"UPDATE lieux SET {set_clause}, updated_at = datetime('now') WHERE id = ?",
            list(fields.values()) + [lieu_id],
        )
        # reset des tables liées pour ré-insertion propre
        for tbl in ("lieu_types", "horaires_tranches", "phrases_accroche", "contacts",
                    "activites_priorite", "ambiance_moment", "ambiance_types",
                    "lieu_services", "lieu_tags", "images"):
            cur.execute(f"DELETE FROM {tbl} WHERE lieu_id = ?", (lieu_id,))

    # --- types de lieu ---
    for type_nom in data.get("types", []):
        type_id = _get_or_create_id(cur, "types_lieu", type_nom)
        cur.execute("INSERT OR IGNORE INTO lieu_types (lieu_id, type_id) VALUES (?, ?)", (lieu_id, type_id))

    # --- horaires ---
    for jour, tranches in (data.get("horaires") or {}).items():
        if not tranches:
            cur.execute(
                "INSERT INTO horaires_tranches (lieu_id, jour, ferme) VALUES (?, ?, 1)",
                (lieu_id, jour),
            )
        else:
            for debut, fin in tranches:
                cur.execute(
                    "INSERT INTO horaires_tranches (lieu_id, jour, ferme, heure_debut, heure_fin) VALUES (?, ?, 0, ?, ?)",
                    (lieu_id, jour, debut, fin),
                )

    # --- phrases d'accroche ---
    for moment, phrase in (data.get("phrases_accroche") or {}).items():
        cur.execute(
            "INSERT INTO phrases_accroche (lieu_id, moment, phrase) VALUES (?, ?, ?)",
            (lieu_id, moment, phrase),
        )

    # --- contact ---
    contact = data.get("contact")
    if contact:
        cur.execute(
            "INSERT INTO contacts (lieu_id, nom, prenom, email, telephone_portable) VALUES (?, ?, ?, ?, ?)",
            (lieu_id, contact.get("nom"), contact.get("prenom"), contact.get("email"), contact.get("telephone_portable")),
        )

    # --- activités par moment ---
    for activite_nom, par_moment in (data.get("activites_priorite") or {}).items():
        cur.execute("SELECT id FROM activites WHERE nom = ?", (activite_nom,))
        row = cur.fetchone()
        if not row:
            continue
        activite_id = row[0]
        for moment, valeur in par_moment.items():
            cur.execute(
                "INSERT INTO activites_priorite (lieu_id, activite_id, moment, valeur) VALUES (?, ?, ?, ?)",
                (lieu_id, activite_id, moment, valeur),
            )

    # --- ambiance par moment ---
    for moment, amb in (data.get("ambiance") or {}).items():
        cur.execute(
            "INSERT INTO ambiance_moment (lieu_id, moment, bruit, luminosite, musique, affluence) VALUES (?, ?, ?, ?, ?, ?)",
            (lieu_id, moment, amb.get("bruit"), amb.get("luminosite"), amb.get("musique"), amb.get("affluence")),
        )
        for amb_type in amb.get("types", []):
            cur.execute(
                "INSERT INTO ambiance_types (lieu_id, moment, ambiance_type) VALUES (?, ?, ?)",
                (lieu_id, moment, amb_type),
            )

    # --- services ---
    for service_nom in data.get("services", []):
        service_id = _get_or_create_id(cur, "services", service_nom)
        cur.execute("INSERT OR IGNORE INTO lieu_services (lieu_id, service_id) VALUES (?, ?)", (lieu_id, service_id))

    # --- tags ---
    for tag_nom in data.get("tags", []):
        tag_id = _get_or_create_id(cur, "tags", tag_nom)
        cur.execute("INSERT OR IGNORE INTO lieu_tags (lieu_id, tag_id) VALUES (?, ?)", (lieu_id, tag_id))

    # --- images ---
    for i, url in enumerate(data.get("images", []), start=1):
        cur.execute("INSERT INTO images (lieu_id, url, ordre) VALUES (?, ?, ?)", (lieu_id, url, i))

    conn.commit()
    conn.close()
    return lieu_id


def get_lieu_summary(lieu_id: int) -> dict:
    """Petite fonction de vérification : relit une fiche complète."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    lieu = dict(cur.execute("SELECT * FROM lieux WHERE id = ?", (lieu_id,)).fetchone())
    lieu["types"] = [r[0] for r in cur.execute(
        "SELECT t.nom FROM types_lieu t JOIN lieu_types lt ON lt.type_id = t.id WHERE lt.lieu_id = ?", (lieu_id,))]
    lieu["services"] = [r[0] for r in cur.execute(
        "SELECT s.nom FROM services s JOIN lieu_services ls ON ls.service_id = s.id WHERE ls.lieu_id = ?", (lieu_id,))]
    lieu["tags"] = [r[0] for r in cur.execute(
        "SELECT tg.nom FROM tags tg JOIN lieu_tags lt ON lt.tag_id = tg.id WHERE lt.lieu_id = ?", (lieu_id,))]
    lieu["horaires"] = [dict(r) for r in cur.execute(
        "SELECT jour, ferme, heure_debut, heure_fin FROM horaires_tranches WHERE lieu_id = ?", (lieu_id,))]
    conn.close()
    return lieu
