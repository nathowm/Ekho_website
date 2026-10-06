/* ════════════════════════════════════════════
   ekho — gestion du consentement aux cookies
   Google Analytics (mesure d'audience), Meta Pixel (publicité) et
   Google Tag Manager ne sont chargés qu'après accord explicite
   (recommandations CNIL).
   Le choix est conservé 6 mois, puis redemandé.
════════════════════════════════════════════ */
(function () {
  var STORAGE_KEY = 'ekho_consent';
  var CONSENT_VERSION = 1;
  var MAX_AGE_MS = 1000 * 60 * 60 * 24 * 182; // ~6 mois
  var META_PIXEL_ID = '1063546799639701';
  var GTM_ID = 'GTM-PHFNZK7H';

  // ── Lecture / écriture du choix ──
  function readConsent() {
    try {
      var c = JSON.parse(localStorage.getItem(STORAGE_KEY));
      if (!c || c.v !== CONSENT_VERSION || Date.now() - c.ts > MAX_AGE_MS) return null;
      return c;
    } catch (e) { return null; }
  }
  function writeConsent(analytics, ads) {
    var c = { v: CONSENT_VERSION, analytics: !!analytics, ads: !!ads, ts: Date.now() };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(c)); } catch (e) {}
    return c;
  }

  // ── Chargement des traceurs ──
  var loaded = { analytics: false, ads: false };

  function ensureGtag() {
    window.dataLayer = window.dataLayer || [];
    if (!window.gtag) window.gtag = function () { dataLayer.push(arguments); };
  }

  // Consent Mode Google : transmet le choix du visiteur à gtag et à Tag Manager
  function setGoogleConsent(c) {
    ensureGtag();
    gtag('consent', 'default', {
      analytics_storage: c.analytics ? 'granted' : 'denied',
      ad_storage: c.ads ? 'granted' : 'denied',
      ad_user_data: c.ads ? 'granted' : 'denied',
      ad_personalization: c.ads ? 'granted' : 'denied'
    });
  }

  // Google Analytics (G-PGSB7B1NYE) est déclenché par le conteneur Tag Manager :
  // ne pas le recharger directement, sinon chaque visite est comptée deux fois.
  // Durée de vie des cookies _ga à limiter à 13 mois dans GTM (maximum CNIL).
  function loadAnalytics(c) {
    if (loaded.analytics) return;
    loaded.analytics = true;
    setGoogleConsent(c);
    dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + GTM_ID;
    document.head.appendChild(s);
  }

  function loadAds() {
    if (loaded.ads) return;
    loaded.ads = true;
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', META_PIXEL_ID);
    fbq('track', 'PageView');
  }

  function apply(c) {
    if (c.analytics) loadAnalytics(c); else clearCookies(['_ga', '_gid', '_gat']);
    if (c.ads) loadAds(); else clearCookies(['_fbp', '_fbc']);
  }

  // Supprime les cookies déposés par un traceur dont le consentement est retiré
  function clearCookies(prefixes) {
    var host = location.hostname;
    var domains = ['', host, '.' + host, '.' + host.replace(/^www\./, '')];
    document.cookie.split(';').forEach(function (raw) {
      var name = raw.split('=')[0].trim();
      if (!prefixes.some(function (p) { return name.indexOf(p) === 0; })) return;
      domains.forEach(function (d) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + (d ? '; domain=' + d : '');
      });
    });
  }

  // ── Interface ──
  var CSS = '' +
    '.ck-banner{position:fixed;left:16px;right:16px;bottom:16px;z-index:1000;max-width:560px;margin:0 auto;' +
      'background:#1A1B2E;color:#fff;border-radius:20px;padding:22px 22px 18px;font-family:Poppins,sans-serif;' +
      'box-shadow:0 18px 50px rgba(14,15,26,.35);border:1px solid rgba(255,255,255,.08)}' +
    '.ck-banner[hidden]{display:none}' +
    '.ck-title{font-size:.95rem;font-weight:800;letter-spacing:-.02em;color:#ECF890;margin-bottom:8px}' +
    '.ck-text{font-size:.78rem;line-height:1.6;color:rgba(255,255,255,.82)}' +
    '.ck-text a{color:#fff;text-decoration:underline}' +
    '.ck-opts{margin-top:14px;display:flex;flex-direction:column;gap:10px}' +
    '.ck-opts[hidden]{display:none}' +
    '.ck-opt{display:flex;align-items:flex-start;gap:12px;padding:12px 14px;border-radius:14px;background:rgba(255,255,255,.06);cursor:pointer}' +
    '.ck-opt input{margin-top:3px;width:18px;height:18px;accent-color:#4B3BB3;flex-shrink:0;cursor:pointer}' +
    '.ck-opt input:disabled{cursor:not-allowed}' +
    '.ck-opt strong{display:block;font-size:.8rem;font-weight:700}' +
    '.ck-opt span{display:block;font-size:.72rem;line-height:1.5;color:rgba(255,255,255,.68);margin-top:2px}' +
    '.ck-actions{margin-top:16px;display:flex;flex-wrap:wrap;gap:8px}' +
    '.ck-btn{flex:1 1 140px;font-family:Poppins,sans-serif;font-size:.78rem;font-weight:700;padding:11px 16px;' +
      'border-radius:100px;cursor:pointer;border:1.5px solid #4B3BB3;background:#4B3BB3;color:#fff;transition:background .2s,border-color .2s}' +
    '.ck-btn:hover{background:#3B2E8F;border-color:#3B2E8F}' +
    '.ck-btn-ghost{background:transparent;border-color:rgba(255,255,255,.35)}' +
    '.ck-btn-ghost:hover{background:rgba(255,255,255,.08);border-color:#fff}' +
    '.ck-btn:focus-visible,.ck-opt input:focus-visible{outline:2px solid #ECF890;outline-offset:2px}' +
    '@media(max-width:480px){.ck-banner{left:12px;right:12px;bottom:12px;padding:18px 16px 14px}.ck-btn{flex-basis:100%}}';

  var HTML = '' +
    '<div class="ck-title" id="ck-title">On respecte ta vie privée 🍪</div>' +
    '<p class="ck-text" id="ck-desc">ekho utilise des cookies pour mesurer l\'audience du site et, si tu l\'acceptes, ' +
      'pour mesurer l\'efficacité de nos publicités sur Facebook et Instagram. Rien n\'est déposé sans ton accord, ' +
      'et tu peux changer d\'avis à tout moment via « Gérer les cookies » en bas de page. ' +
      '<a href="/politique-de-confidentialite#cookies">En savoir plus</a></p>' +
    '<div class="ck-opts" hidden>' +
      '<label class="ck-opt"><input type="checkbox" checked disabled/>' +
        '<div><strong>Strictement nécessaires</strong><span>Mémoriser ton choix de cookies. Toujours actifs.</span></div></label>' +
      '<label class="ck-opt"><input type="checkbox" data-ck="analytics"/>' +
        '<div><strong>Mesure d\'audience — Google Analytics</strong><span>Savoir combien de personnes visitent le site et quelles pages les intéressent.</span></div></label>' +
      '<label class="ck-opt"><input type="checkbox" data-ck="ads"/>' +
        '<div><strong>Publicité — Meta Pixel</strong><span>Mesurer et améliorer nos campagnes sur Facebook et Instagram.</span></div></label>' +
    '</div>' +
    '<div class="ck-actions">' +
      '<button type="button" class="ck-btn ck-btn-ghost" data-ck-action="refuse">Tout refuser</button>' +
      '<button type="button" class="ck-btn ck-btn-ghost" data-ck-action="custom">Personnaliser</button>' +
      '<button type="button" class="ck-btn" data-ck-action="accept">Tout accepter</button>' +
    '</div>';

  var banner;

  function buildBanner() {
    if (banner) return banner;
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);
    banner = document.createElement('div');
    banner.className = 'ck-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-labelledby', 'ck-title');
    banner.setAttribute('aria-describedby', 'ck-desc');
    banner.hidden = true;
    banner.innerHTML = HTML;
    document.body.appendChild(banner);

    banner.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-ck-action]');
      if (!btn) return;
      var action = btn.getAttribute('data-ck-action');
      if (action === 'accept') return save(true, true);
      if (action === 'refuse') return save(false, false);
      if (action === 'custom') return showOptions();
      if (action === 'save') {
        save(banner.querySelector('[data-ck="analytics"]').checked,
             banner.querySelector('[data-ck="ads"]').checked);
      }
    });
    return banner;
  }

  function showOptions() {
    banner.querySelector('.ck-opts').hidden = false;
    var custom = banner.querySelector('[data-ck-action="custom"]');
    custom.textContent = 'Enregistrer mes choix';
    custom.setAttribute('data-ck-action', 'save');
  }

  function openBanner(withOptions) {
    buildBanner();
    var c = readConsent();
    banner.querySelector('[data-ck="analytics"]').checked = !!(c && c.analytics);
    banner.querySelector('[data-ck="ads"]').checked = !!(c && c.ads);
    if (withOptions) showOptions();
    banner.hidden = false;
    if (withOptions) banner.querySelector('.ck-btn').focus({ preventScroll: true });
  }

  function save(analytics, ads) {
    var prev = readConsent();
    var c = writeConsent(analytics, ads);
    banner.hidden = true;
    // Consentement retiré pour un traceur déjà chargé : on nettoie et on recharge
    var withdrawn = (prev && prev.analytics && !c.analytics) || (prev && prev.ads && !c.ads) ||
                    (loaded.analytics && !c.analytics) || (loaded.ads && !c.ads);
    if (withdrawn) {
      // Le rechargement décharge les scripts ; apply() supprime ensuite leurs cookies
      location.reload();
      return;
    }
    apply(c);
  }

  // ── Démarrage ──
  function init() {
    var c = readConsent();
    if (c) apply(c); else openBanner(false);

    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-cookie-settings]');
      if (!link) return;
      e.preventDefault();
      openBanner(true);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
