"""
Génère une visualisation HTML autonome (lieux_viewer.html) de la base
miroir locale, avec un formulaire "Ajouter un lieu" intégré (stockage
navigateur local via localStorage). À relancer après chaque ajout/modif
de lieu côté base SQLite pour rafraîchir le "socle" de données.

Les lieux ajoutés depuis le formulaire HTML restent uniquement dans le
navigateur (localStorage) tant qu'ils n'ont pas été resynchronisés dans
lieux_mirror.db (bouton "Exporter les ajouts locaux (JSON)" -> renvoyer
le fichier pour intégration définitive dans la base).

Usage :
    python3 export_html.py
"""
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "lieux_mirror.db"
OUT_PATH = Path(__file__).parent / "lieux_viewer.html"

MOMENTS = ["Matin", "Midi", "Après-midi", "Soir"]
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


def fetch_all_lieux():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    lieux = [dict(r) for r in cur.execute("SELECT * FROM lieux ORDER BY nom")]

    for lieu in lieux:
        lid = lieu["id"]
        lieu["origin"] = "db"

        lieu["types"] = [r[0] for r in cur.execute(
            "SELECT t.nom FROM types_lieu t JOIN lieu_types lt ON lt.type_id=t.id WHERE lt.lieu_id=?", (lid,))]

        horaires = {j: None for j in JOURS}
        for r in cur.execute(
                "SELECT jour, ferme, heure_debut, heure_fin FROM horaires_tranches WHERE lieu_id=? ORDER BY id", (lid,)):
            j, ferme, debut, fin = r
            if ferme:
                horaires[j] = "Fermé"
            else:
                tranche = f"{debut}–{fin}"
                horaires[j] = tranche if not horaires[j] or horaires[j] == "Fermé" else horaires[j] + ", " + tranche
        lieu["horaires"] = horaires

        lieu["phrases_accroche"] = {m: None for m in MOMENTS}
        for moment, phrase in cur.execute(
                "SELECT moment, phrase FROM phrases_accroche WHERE lieu_id=?", (lid,)):
            lieu["phrases_accroche"][moment] = phrase

        contact = cur.execute(
            "SELECT nom, prenom, email, telephone_portable FROM contacts WHERE lieu_id=?", (lid,)).fetchone()
        lieu["contact"] = dict(contact) if contact else None

        activites = {}
        for nom, moment, valeur in cur.execute(
                """SELECT a.nom, ap.moment, ap.valeur FROM activites_priorite ap
                   JOIN activites a ON a.id = ap.activite_id WHERE ap.lieu_id=?""", (lid,)):
            activites.setdefault(nom, {})[moment] = valeur
        lieu["activites_priorite"] = activites

        ambiance = {}
        for row in cur.execute(
                "SELECT moment, bruit, luminosite, musique, affluence FROM ambiance_moment WHERE lieu_id=?", (lid,)):
            m, bruit, lum, mus, aff = row
            ambiance[m] = {"bruit": bruit, "luminosite": lum, "musique": mus, "affluence": aff, "types": []}
        for m, t in cur.execute("SELECT moment, ambiance_type FROM ambiance_types WHERE lieu_id=?", (lid,)):
            ambiance.setdefault(m, {"bruit": None, "luminosite": None, "musique": None, "affluence": None, "types": []})
            ambiance[m]["types"].append(t)
        lieu["ambiance"] = ambiance

        lieu["services"] = [r[0] for r in cur.execute(
            "SELECT s.nom FROM services s JOIN lieu_services ls ON ls.service_id=s.id WHERE ls.lieu_id=?", (lid,))]

        lieu["tags"] = [r[0] for r in cur.execute(
            "SELECT tg.nom FROM tags tg JOIN lieu_tags lt ON lt.tag_id=tg.id WHERE lt.lieu_id=?", (lid,))]

        lieu["images"] = [r[0] for r in cur.execute(
            "SELECT url FROM images WHERE lieu_id=? ORDER BY ordre", (lid,))]

    ref_types = [r[0] for r in cur.execute("SELECT nom FROM types_lieu ORDER BY nom")]
    ref_services = [r[0] for r in cur.execute("SELECT nom FROM services ORDER BY nom")]
    ref_tags = [r[0] for r in cur.execute("SELECT nom FROM tags ORDER BY nom")]

    conn.close()
    return lieux, ref_types, ref_services, ref_tags


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Base miroir — Lieux</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {
    --bg: #f5f6f8; --panel: #ffffff; --border: #e3e5e9; --text: #1c1f24;
    --muted: #6b7280; --accent: #2f6f4f; --accent-light: #e8f3ec;
    --chip: #eef0f3; --danger: #b3441c; --warn: #a06a00; --warn-light: #fbf1de;
  }
  * { box-sizing: border-box; }
  html, body { height:100%; margin:0; overflow:hidden; }
  body { font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); display:flex; flex-direction:column; }
  header { flex-shrink:0; padding: 20px 28px; border-bottom: 1px solid var(--border); background: var(--panel); display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; }
  header h1 { font-size: 18px; margin:0; }
  header .count { color: var(--muted); font-size: 13px; }
  .header-actions { display:flex; gap:8px; flex-wrap:wrap; }
  button { font-family: inherit; cursor:pointer; }
  .btn { padding:9px 14px; border-radius:8px; border:1px solid var(--border); background: var(--panel); font-size:13px; font-weight:500; }
  .btn:hover { background: var(--chip); }
  .btn-primary { background: var(--accent); color:#fff; border-color: var(--accent); }
  .btn-primary:hover { background:#26603f; }
  .btn-danger { color: var(--danger); }
  .layout { display: flex; flex:1; min-height:0; overflow:hidden; }
  .sidebar { width: 300px; flex-shrink:0; border-right: 1px solid var(--border); background: var(--panel); padding: 16px; overflow-y:auto; height:100%; }
  .search { width:100%; padding:9px 12px; border:1px solid var(--border); border-radius:8px; font-size:14px; margin-bottom:10px; }
  .lieu-item { padding:12px; border-radius:10px; cursor:pointer; margin-bottom:6px; border:1px solid transparent; }
  .lieu-item:hover { background: var(--chip); }
  .lieu-item.active { background: var(--accent-light); border-color: var(--accent); }
  .lieu-item .nom { font-weight:600; font-size:14px; }
  .lieu-item .sub { font-size:12px; color: var(--muted); margin-top:2px; }
  .badge { display:inline-block; font-size:10px; padding:2px 6px; border-radius:5px; margin-top:6px; margin-right:4px; }
  .badge.actif { background:#e8f3ec; color:var(--accent); }
  .badge.inactif { background:#f2e6e2; color:var(--danger); }
  .badge.local { background: var(--warn-light); color: var(--warn); }
  .badge.partner { background:#fff3b0; color:#7a5c00; font-weight:600; }
  .chip.partner { background:#fff3b0; color:#7a5c00; font-weight:600; }
  main { flex:1; padding: 28px; overflow-y:auto; height:100%; }
  .empty { color: var(--muted); text-align:center; margin-top:80px; }
  .card-header { display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:14px; margin-bottom:20px; }
  .card-header h2 { margin:0 0 6px 0; font-size: 24px; }
  .card-header .addr { color: var(--muted); font-size: 14px; }
  .chips { display:flex; flex-wrap:wrap; gap:6px; margin-top:8px; }
  .chip { background: var(--chip); border-radius:20px; padding:4px 12px; font-size:12px; }
  .chip.tag { background: var(--accent-light); color: var(--accent); }
  .section { background: var(--panel); border:1px solid var(--border); border-radius:12px; padding:18px 20px; margin-bottom:16px; }
  .section h3 { margin:0 0 12px 0; font-size:14px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }
  .grid-2 { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap:12px; }
  .kv { font-size:13px; }
  .kv .k { color: var(--muted); }
  .kv .v { font-weight:500; }
  table { width:100%; border-collapse: collapse; font-size:13px; }
  th, td { text-align:left; padding:6px 8px; border-bottom:1px solid var(--border); }
  th { color: var(--muted); font-weight:600; }
  .closed { color: var(--danger); }
  .scale-cell { text-align:center; font-weight:700; }
  .scale-P, .scale-F { color: var(--accent); }
  .scale-S, .scale-O { color: #b58900; }
  .scale-dash, .scale-R { color: var(--muted); }
  .images { display:flex; gap:10px; flex-wrap:wrap; }
  .images img { width:150px; height:110px; object-fit:cover; border-radius:8px; border:1px solid var(--border); }
  .phrase { font-style: italic; font-size:13px; margin-bottom:8px; }
  .phrase b { font-style: normal; color: var(--muted); font-size:11px; text-transform:uppercase; margin-right:6px; }
  .source { font-size:11px; color: var(--muted); margin-top:20px; }
  a { color: var(--accent); }

  /* Modal formulaire */
  .overlay { display:none; position:fixed; inset:0; background:rgba(20,22,26,.45); z-index:50; align-items:flex-start; justify-content:center; padding:40px 20px; overflow-y:auto; }
  .overlay.open { display:flex; }
  .modal { background:var(--panel); border-radius:14px; width:100%; max-width:720px; padding:0; max-height: calc(100vh - 80px); display:flex; flex-direction:column; }
  .modal-header { padding:18px 24px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; }
  .modal-header h2 { margin:0; font-size:17px; }
  .modal-body { padding:20px 24px; overflow-y:auto; }
  .modal-footer { padding:16px 24px; border-top:1px solid var(--border); display:flex; justify-content:flex-end; gap:10px; }
  .close-x { background:none; border:none; font-size:20px; color:var(--muted); }
  .form-section { margin-bottom:22px; }
  .form-section h4 { font-size:12px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); margin:0 0 10px 0; }
  .field { margin-bottom:10px; }
  .field label { display:block; font-size:12px; color:var(--muted); margin-bottom:4px; }
  .field input[type=text], .field input[type=number], .field input[type=time], .field select, .field textarea {
    width:100%; padding:8px 10px; border:1px solid var(--border); border-radius:7px; font-size:13px; font-family:inherit;
  }
  .field textarea { resize: vertical; min-height:46px; }
  .checkline { display:flex; align-items:center; gap:6px; font-size:13px; }
  .checkbox-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(140px,1fr)); gap:6px; }
  .hint { font-size:11px; color:var(--muted); margin-top:4px; }
  .btn-sm { padding:4px 10px; font-size:12px; border-radius:6px; }
  .day-block { border:1px solid var(--border); border-radius:9px; padding:10px 12px; margin-bottom:8px; }
  .day-block-header { display:flex; align-items:center; gap:14px; margin-bottom:6px; }
  .day-block-header .day-name { font-weight:600; font-size:13px; width:80px; }
  .day-block-header .add-tranche { margin-left:auto; }
  .tranches.hidden { display:none; }
  .tranche-row { display:flex; align-items:center; gap:8px; margin-bottom:6px; }
  .tranche-row input[type=time] { width:120px; padding:6px 8px; border:1px solid var(--border); border-radius:6px; font-size:13px; }
  .tranche-row .remove-tranche { background:none; border:none; color:var(--danger); font-size:14px; padding:2px 6px; }
</style>
</head>
<body>
<header>
  <h1>🗺️ Base miroir — Lieux</h1>
  <div class="header-actions">
    <span class="count" id="count"></span>
    <button class="btn" id="btn-export" title="Télécharger les lieux ajoutés depuis ce navigateur, à renvoyer pour intégration définitive dans la base SQLite">⬇️ Exporter les ajouts locaux (JSON)</button>
    <button class="btn btn-primary" id="btn-open-form">+ Ajouter un lieu</button>
  </div>
</header>
<div class="layout">
  <div class="sidebar">
    <input class="search" id="search" placeholder="Rechercher un lieu, un quartier...">
    <div id="lieu-list"></div>
  </div>
  <main id="main"></main>
</div>

<!-- Overlay formulaire d'ajout -->
<div class="overlay" id="overlay">
  <div class="modal">
    <div class="modal-header">
      <h2>Ajouter un lieu</h2>
      <button class="close-x" id="btn-close-form">✕</button>
    </div>
    <div class="modal-body" id="form-body">
      <!-- généré par JS -->
    </div>
    <div class="modal-footer">
      <button class="btn" id="btn-cancel-form">Annuler</button>
      <button class="btn btn-primary" id="btn-save-form">Enregistrer le lieu</button>
    </div>
  </div>
</div>

<script>
const DB_DATA = __DATA_JSON__;
const REF_TYPES = __REF_TYPES_JSON__;
const REF_SERVICES = __REF_SERVICES_JSON__;
const REF_TAGS = __REF_TAGS_JSON__;
const MOMENTS = ["Matin","Midi","Après-midi","Soir"];
const JOURS = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"];
const LS_KEY = "lieux_manuels_v1";

let manualLieux = [];
try { manualLieux = JSON.parse(localStorage.getItem(LS_KEY) || "[]"); } catch(e) { manualLieux = []; }

let current = null;

function allLieux() { return DB_DATA.concat(manualLieux); }

function saveManual() { localStorage.setItem(LS_KEY, JSON.stringify(manualLieux)); }

function renderList(filter) {
  const list = document.getElementById('lieu-list');
  const data = allLieux();
  if (current === null) current = data.length ? data[0].id : null;
  const f = (filter || '').toLowerCase();
  const filtered = data.filter(l =>
    l.nom.toLowerCase().includes(f) ||
    (l.quartier||'').toLowerCase().includes(f) ||
    (l.adresse||'').toLowerCase().includes(f)
  );
  document.getElementById('count').textContent = data.length + ' lieu' + (data.length>1?'x':'') + ' dans la base';
  list.innerHTML = filtered.map(l => `
    <div class="lieu-item ${l.id===current?'active':''}" onclick="selectLieu('${l.id}')">
      <div class="nom">${l.nom}</div>
      <div class="sub">${l.quartier || l.arrondissement || ''} — ${(l.types||[]).join(', ')}</div>
      <span class="badge ${l.lieu_actif?'actif':'inactif'}">${l.lieu_actif?'Actif':'Inactif'}</span>
      ${l.partenaire ? '<span class="badge partner" title="Partenaire EKHO">⭐ Partenaire</span>' : ''}
      ${l.origin==='manual' ? '<span class="badge local">Ajout local</span>' : ''}
    </div>
  `).join('') || '<div class="empty">Aucun résultat</div>';
}

function selectLieu(id) {
  current = (typeof id === 'string' && !id.startsWith('local-')) ? (isNaN(id) ? id : Number(id)) : id;
  renderList(document.getElementById('search').value);
  renderMain();
}

function scaleClass(v) {
  if (v === 'P') return 'scale-P';
  if (v === 'S') return 'scale-S';
  if (v === 'F') return 'scale-F';
  if (v === 'O') return 'scale-O';
  if (v === 'R') return 'scale-R';
  return 'scale-dash';
}

function deleteManual(id) {
  if (!confirm('Supprimer ce lieu ajouté localement ?')) return;
  manualLieux = manualLieux.filter(l => l.id !== id);
  saveManual();
  current = allLieux().length ? allLieux()[0].id : null;
  renderList(document.getElementById('search').value);
  renderMain();
}

function renderMain() {
  const main = document.getElementById('main');
  const l = allLieux().find(x => x.id === current);
  if (!l) { main.innerHTML = '<div class="empty">Sélectionne un lieu à gauche, ou clique sur "+ Ajouter un lieu"</div>'; return; }

  const horairesRows = JOURS.map(j => {
    const val = l.horaires[j];
    const isClosed = !val || val === 'Fermé';
    return `<tr><td>${j}</td><td class="${isClosed?'closed':''}">${isClosed ? 'Fermé' : val}</td></tr>`;
  }).join('');

  const phrases = MOMENTS.filter(m => l.phrases_accroche[m]).map(m =>
    `<div class="phrase"><b>${m}</b>${l.phrases_accroche[m]}</div>`).join('') || '<span style="color:var(--muted);font-size:13px;">Aucune renseignée</span>';

  let activitesTable = '';
  const activiteNoms = Object.keys(l.activites_priorite || {});
  if (activiteNoms.length) {
    activitesTable = `<table><tr><th>Activité</th>${MOMENTS.map(m=>`<th>${m}</th>`).join('')}</tr>` +
      activiteNoms.map(nom => {
        const row = l.activites_priorite[nom];
        return `<tr><td>${nom}</td>${MOMENTS.map(m => `<td class="scale-cell ${scaleClass(row[m])}">${row[m]||'–'}</td>`).join('')}</tr>`;
      }).join('') + '</table>';
  } else {
    activitesTable = '<span style="color:var(--muted);font-size:13px;">Non renseigné</span>';
  }

  let ambianceTable = '';
  const ambianceMoments = Object.keys(l.ambiance || {});
  if (ambianceMoments.length) {
    ambianceTable = `<table><tr><th>Moment</th><th>Bruit</th><th>Luminosité</th><th>Musique</th><th>Ambiance</th><th>Affluence</th></tr>` +
      MOMENTS.filter(m => l.ambiance[m]).map(m => {
        const a = l.ambiance[m];
        return `<tr><td>${m}</td><td>${a.bruit||'–'}</td><td>${a.luminosite||'–'}</td><td>${a.musique||'–'}</td><td>${(a.types||[]).join(', ')||'–'}</td><td>${a.affluence||'–'}</td></tr>`;
      }).join('') + '</table>';
  } else {
    ambianceTable = '<span style="color:var(--muted);font-size:13px;">Non renseigné</span>';
  }

  const contact = l.contact ? `
    <div class="grid-2">
      <div class="kv"><div class="k">Nom</div><div class="v">${l.contact.prenom||''} ${l.contact.nom||''}</div></div>
      <div class="kv"><div class="k">Email</div><div class="v">${l.contact.email||'–'}</div></div>
      <div class="kv"><div class="k">Téléphone</div><div class="v">${l.contact.telephone_portable||'–'}</div></div>
    </div>` : '<span style="color:var(--muted);font-size:13px;">Non renseigné</span>';

  const images = (l.images||[]).length ? `<div class="images">${l.images.map(u=>`<img src="${u}" onerror="this.style.display='none'">`).join('')}</div>` : '<span style="color:var(--muted);font-size:13px;">Aucune image</span>';

  main.innerHTML = `
    <div class="card-header">
      <div>
        <h2>${l.nom}</h2>
        <div class="addr">${l.adresse || ''}${l.code_postal ? ' · '+l.code_postal : ''}${l.quartier ? ' · '+l.quartier : ''}</div>
        <div class="chips">
          ${(l.types||[]).map(t=>`<span class="chip">${t}</span>`).join('')}
          <span class="chip">${l.lieu_actif ? '✅ Actif' : '⏸️ Inactif'}</span>
          ${l.partenaire ? '<span class="chip partner">⭐ Partenaire EKHO</span>' : ''}
          ${l.origin==='manual' ? '<span class="chip" style="background:var(--warn-light);color:var(--warn);">🟡 Ajouté localement — non synchronisé avec la base</span>' : ''}
        </div>
      </div>
      ${l.origin==='manual' ? `<button class="btn btn-danger" onclick="deleteManual('${l.id}')">🗑 Supprimer</button>` : ''}
    </div>

    <div class="section">
      <h3>Informations générales</h3>
      <div class="grid-2">
        <div class="kv"><div class="k">Note Google</div><div class="v">${l.note_google ?? '–'} ${l.nombre_avis_google ? '('+l.nombre_avis_google+' avis)' : ''}</div></div>
        <div class="kv"><div class="k">Téléphone public</div><div class="v">${l.telephone_public || '–'}</div></div>
        <div class="kv"><div class="k">Site web</div><div class="v">${l.site_web ? `<a href="${l.site_web}" target="_blank">${l.site_web}</a>` : '–'}</div></div>
        <div class="kv"><div class="k">Lien Google Maps</div><div class="v">${l.lien_google_maps ? `<a href="${l.lien_google_maps}" target="_blank">Voir</a>` : '–'}</div></div>
        <div class="kv"><div class="k">Coordonnées GPS</div><div class="v">${l.latitude ?? '–'}, ${l.longitude ?? '–'}</div></div>
        <div class="kv"><div class="k">Cadre</div><div class="v">${l.cadre || '–'}</div></div>
        <div class="kv"><div class="k">Gamme de prix</div><div class="v">${l.gamme_prix || '–'}</div></div>
        <div class="kv"><div class="k">Niveau d'engagement</div><div class="v">${l.niveau_engagement || '–'}</div></div>
      </div>
    </div>

    <div class="section">
      <h3>Horaires d'ouverture</h3>
      <table>${horairesRows}</table>
    </div>

    <div class="section">
      <h3>Phrases d'accroche</h3>
      ${phrases}
    </div>

    <div class="section">
      <h3>Point de contact</h3>
      ${contact}
    </div>

    <div class="section">
      <h3>Activités principales par moment</h3>
      ${activitesTable}
    </div>

    <div class="section">
      <h3>Ambiance par moment</h3>
      ${ambianceTable}
    </div>

    <div class="section">
      <h3>Services disponibles</h3>
      <div class="chips">${(l.services||[]).map(s=>`<span class="chip">${s}</span>`).join('') || '<span style="color:var(--muted);font-size:13px;">Aucun renseigné</span>'}</div>
    </div>

    <div class="section">
      <h3>Reconnu pour</h3>
      <div class="chips">${(l.tags||[]).map(t=>`<span class="chip tag">${t}</span>`).join('') || '<span style="color:var(--muted);font-size:13px;">Aucun tag</span>'}</div>
    </div>

    <div class="section">
      <h3>Images</h3>
      ${images}
    </div>

    ${l.source_donnees ? `<div class="source">Source des données : ${l.source_donnees}</div>` : ''}
  `;
}

/* ---------------------- Formulaire d'ajout ---------------------- */

function buildFormHTML() {
  const typeChecks = REF_TYPES.map(t => `<label class="checkline"><input type="checkbox" name="types" value="${t}"> ${t}</label>`).join('');
  const serviceChecks = REF_SERVICES.map(s => `<label class="checkline"><input type="checkbox" name="services" value="${s}"> ${s}</label>`).join('');
  const dayRows = JOURS.map(j => `
    <div class="day-block" data-day="${j}">
      <div class="day-block-header">
        <span class="day-name">${j}</span>
        <label class="checkline"><input type="checkbox" data-day="${j}" class="jour-ferme"> Fermé</label>
        <button type="button" class="btn btn-sm add-tranche" data-day="${j}">+ Ajouter tranche</button>
      </div>
      <div class="tranches" data-day="${j}">
        <div class="tranche-row">
          <input type="time" class="tranche-debut" value="09:00">
          <span>à</span>
          <input type="time" class="tranche-fin" value="19:00">
          <button type="button" class="remove-tranche" title="Retirer cette tranche">✕</button>
        </div>
      </div>
    </div>`).join('');

  return `
    <div class="form-section">
      <h4>Informations générales</h4>
      <div class="field"><label>Nom du lieu *</label><input type="text" id="f-nom" placeholder="Ex : Le Petit Café"></div>
      <div class="field"><label>Type(s) de lieu</label><div class="checkbox-grid">${typeChecks}</div></div>
      <div class="grid-2">
        <label class="checkline"><input type="checkbox" id="f-partenaire"> Partenaire</label>
        <label class="checkline"><input type="checkbox" id="f-actif" checked> Lieu actif</label>
      </div>
    </div>

    <div class="form-section">
      <h4>Localisation</h4>
      <div class="grid-2">
        <div class="field"><label>Code postal</label><input type="text" id="f-cp"></div>
        <div class="field"><label>Arrondissement</label><input type="text" id="f-arrdt" placeholder="Ex : 1er"></div>
        <div class="field"><label>Quartier</label><input type="text" id="f-quartier"></div>
        <div class="field"><label>Adresse</label><input type="text" id="f-adresse"></div>
        <div class="field"><label>Latitude</label><input type="number" step="0.0001" id="f-lat"></div>
        <div class="field"><label>Longitude</label><input type="number" step="0.0001" id="f-lng"></div>
      </div>
      <div class="field"><label>Lien Google Maps</label><input type="text" id="f-gmaps" placeholder="https://maps.app.goo.gl/..."></div>
    </div>

    <div class="form-section">
      <h4>Contact public & réputation</h4>
      <div class="grid-2">
        <div class="field"><label>Note Google</label><input type="number" step="0.1" min="0" max="5" id="f-note"></div>
        <div class="field"><label>Nombre d'avis Google</label><input type="number" id="f-avis"></div>
        <div class="field"><label>Téléphone (public)</label><input type="text" id="f-tel"></div>
        <div class="field"><label>Site web</label><input type="text" id="f-site" placeholder="https://..."></div>
      </div>
    </div>

    <div class="form-section">
      <h4>Horaires d'ouverture</h4>
      ${dayRows}
      <div class="hint">Plusieurs tranches possibles par jour (ex : 8h-14h puis 18h-23h). Pour un service qui finit après minuit, utilise une tranche dont l'heure de fin est inférieure à l'heure de début.</div>
    </div>

    <div class="form-section">
      <h4>Phrases d'accroche</h4>
      <div class="grid-2">
        <div class="field"><label>Matin</label><textarea id="f-phrase-matin"></textarea></div>
        <div class="field"><label>Midi</label><textarea id="f-phrase-midi"></textarea></div>
        <div class="field"><label>Après-midi</label><textarea id="f-phrase-apresmidi"></textarea></div>
        <div class="field"><label>Soir</label><textarea id="f-phrase-soir"></textarea></div>
      </div>
    </div>

    <div class="form-section">
      <h4>Autres attributs</h4>
      <div class="grid-2">
        <div class="field"><label>Cadre</label>
          <select id="f-cadre">
            <option value="">-- Non renseigné --</option>
            <option>Intérieur</option>
            <option>Extérieur</option>
            <option>Mixte</option>
          </select>
        </div>
        <div class="field"><label>Gamme de prix</label><input type="text" id="f-prix" placeholder="Ex : €, €€, €€€"></div>
      </div>
    </div>

    <div class="form-section">
      <h4>Services disponibles</h4>
      <div class="checkbox-grid">${serviceChecks}</div>
    </div>

    <div class="form-section">
      <h4>Reconnu pour (tags)</h4>
      <div class="field">
        <input type="text" id="f-tags" placeholder="Ex : Cosy, Café Spécialisé, Brunch...">
        <div class="hint">Propose librement les tags les plus pertinents pour ce lieu, séparés par des virgules — pas besoin de te limiter à une liste existante.</div>
      </div>
    </div>

    <div class="form-section">
      <h4>Images</h4>
      <div class="field"><label>URLs des images (une par ligne, la 1ère = couverture)</label><textarea id="f-images" rows="3"></textarea></div>
    </div>

    <div class="form-section">
      <h4>Source des données</h4>
      <div class="field"><textarea id="f-source" placeholder="Ex : recherche web du 13/07/2026, site officiel, Instagram..."></textarea></div>
    </div>
  `;
}

function makeTrancheRow(debut, fin) {
  const row = document.createElement('div');
  row.className = 'tranche-row';
  row.innerHTML = `
    <input type="time" class="tranche-debut" value="${debut||'09:00'}">
    <span>à</span>
    <input type="time" class="tranche-fin" value="${fin||'19:00'}">
    <button type="button" class="remove-tranche" title="Retirer cette tranche">✕</button>`;
  return row;
}

function openForm() {
  document.getElementById('form-body').innerHTML = buildFormHTML();
  document.getElementById('overlay').classList.add('open');

  // Ajouter une tranche horaire pour un jour donné
  document.querySelectorAll('.add-tranche').forEach(btn => {
    btn.addEventListener('click', () => {
      const day = btn.dataset.day;
      const container = document.querySelector(`.tranches[data-day="${day}"]`);
      container.appendChild(makeTrancheRow('09:00', '19:00'));
    });
  });

  // Cocher "Fermé" masque les tranches de ce jour
  document.querySelectorAll('.jour-ferme').forEach(cb => {
    cb.addEventListener('change', () => {
      const day = cb.dataset.day;
      document.querySelector(`.tranches[data-day="${day}"]`).classList.toggle('hidden', cb.checked);
    });
  });

  // Retirer une tranche (délégation, car les lignes sont ajoutées dynamiquement)
  document.getElementById('form-body').addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-tranche')) {
      const row = e.target.closest('.tranche-row');
      const container = row.parentElement;
      if (container.children.length > 1) row.remove();
      else row.remove(); // autorise aussi 0 tranche = horaires non renseignés ce jour-là
    }
  });
}
function closeForm() { document.getElementById('overlay').classList.remove('open'); }

function collectChecked(name) {
  return Array.from(document.querySelectorAll(`input[name="${name}"]:checked`)).map(el => el.value);
}

function saveForm() {
  const nom = document.getElementById('f-nom').value.trim();
  if (!nom) { alert('Le nom du lieu est obligatoire.'); return; }

  const horaires = {};
  JOURS.forEach(j => {
    const ferme = document.querySelector(`.jour-ferme[data-day="${j}"]`).checked;
    if (ferme) { horaires[j] = 'Fermé'; return; }
    const container = document.querySelector(`.tranches[data-day="${j}"]`);
    const tranches = Array.from(container.querySelectorAll('.tranche-row')).map(row => {
      const debut = row.querySelector('.tranche-debut').value;
      const fin = row.querySelector('.tranche-fin').value;
      return (debut && fin) ? `${debut}–${fin}` : null;
    }).filter(Boolean);
    horaires[j] = tranches.length ? tranches.join(', ') : null;
  });

  const phrases_accroche = {
    "Matin": document.getElementById('f-phrase-matin').value.trim() || null,
    "Midi": document.getElementById('f-phrase-midi').value.trim() || null,
    "Après-midi": document.getElementById('f-phrase-apresmidi').value.trim() || null,
    "Soir": document.getElementById('f-phrase-soir').value.trim() || null,
  };

  const tags = document.getElementById('f-tags').value.split(',').map(t => t.trim()).filter(Boolean);
  const images = document.getElementById('f-images').value.split('\\n').map(u => u.trim()).filter(Boolean);

  const lieu = {
    id: 'local-' + Date.now(),
    origin: 'manual',
    nom,
    partenaire: document.getElementById('f-partenaire').checked ? 1 : 0,
    lieu_actif: document.getElementById('f-actif').checked ? 1 : 0,
    types: collectChecked('types'),
    code_postal: document.getElementById('f-cp').value.trim() || null,
    arrondissement: document.getElementById('f-arrdt').value.trim() || null,
    quartier: document.getElementById('f-quartier').value.trim() || null,
    adresse: document.getElementById('f-adresse').value.trim() || null,
    latitude: document.getElementById('f-lat').value ? parseFloat(document.getElementById('f-lat').value) : null,
    longitude: document.getElementById('f-lng').value ? parseFloat(document.getElementById('f-lng').value) : null,
    lien_google_maps: document.getElementById('f-gmaps').value.trim() || null,
    note_google: document.getElementById('f-note').value ? parseFloat(document.getElementById('f-note').value) : null,
    nombre_avis_google: document.getElementById('f-avis').value ? parseInt(document.getElementById('f-avis').value) : null,
    site_web: document.getElementById('f-site').value.trim() || null,
    telephone_public: document.getElementById('f-tel').value.trim() || null,
    niveau_engagement: null,
    gamme_prix: document.getElementById('f-prix').value.trim() || null,
    cadre: document.getElementById('f-cadre').value || null,
    source_donnees: document.getElementById('f-source').value.trim() || 'Ajouté manuellement depuis le formulaire HTML',
    horaires,
    phrases_accroche,
    contact: null,
    activites_priorite: {},
    ambiance: {},
    services: collectChecked('services'),
    tags,
    images,
  };

  manualLieux.push(lieu);
  saveManual();
  closeForm();
  current = lieu.id;
  renderList('');
  document.getElementById('search').value = '';
  renderMain();
}

function exportManual() {
  if (!manualLieux.length) { alert('Aucun lieu ajouté localement pour le moment.'); return; }
  const blob = new Blob([JSON.stringify(manualLieux, null, 2)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'lieux_ajouts_locaux.json';
  a.click();
}

document.getElementById('search').addEventListener('input', e => renderList(e.target.value));
document.getElementById('btn-open-form').addEventListener('click', openForm);
document.getElementById('btn-close-form').addEventListener('click', closeForm);
document.getElementById('btn-cancel-form').addEventListener('click', closeForm);
document.getElementById('btn-save-form').addEventListener('click', saveForm);
document.getElementById('btn-export').addEventListener('click', exportManual);
document.getElementById('overlay').addEventListener('click', e => { if (e.target.id === 'overlay') closeForm(); });

renderList('');
renderMain();
</script>
</body>
</html>
"""


def export_html():
    lieux, ref_types, ref_services, ref_tags = fetch_all_lieux()
    html = (HTML_TEMPLATE
            .replace("__DATA_JSON__", json.dumps(lieux, ensure_ascii=False))
            .replace("__REF_TYPES_JSON__", json.dumps(ref_types, ensure_ascii=False))
            .replace("__REF_SERVICES_JSON__", json.dumps(ref_services, ensure_ascii=False))
            .replace("__REF_TAGS_JSON__", json.dumps(ref_tags, ensure_ascii=False)))
    OUT_PATH.write_text(html, encoding="utf-8")
    print(f"Vue HTML générée : {OUT_PATH} ({len(lieux)} lieu(x) en base)")


if __name__ == "__main__":
    export_html()
