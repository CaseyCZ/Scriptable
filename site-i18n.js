// Scriptable Apps UI translations — CZ / EN / DE / ES / FR
(() => {
  'use strict';

  const TEXT = {
    'Our apps': {de:'Unsere Apps', es:'Nuestras apps', fr:'Nos apps'},
    'Community': {de:'Community', es:'Comunidad', fr:'Communauté'},
    'Settings': {de:'Einstellungen', es:'Ajustes', fr:'Paramètres'},
    'APPEARANCE': {de:'DARSTELLUNG', es:'APARIENCIA', fr:'APPARENCE'},
    'Dark': {de:'Dunkel', es:'Oscuro', fr:'Sombre'},
    'Light': {de:'Hell', es:'Claro', fr:'Clair'},
    'LANGUAGE': {de:'SPRACHE', es:'IDIOMA', fr:'LANGUE'},
    'LAYOUT': {de:'LAYOUT', es:'DISEÑO', fr:'MISE EN PAGE'},
    'REPORT ISSUE': {de:'PROBLEM MELDEN', es:'INFORMAR DE UN PROBLEMA', fr:'SIGNALER UN PROBLÈME'},
    'Report issue': {de:'Problem melden', es:'Informar de un problema', fr:'Signaler un problème'},
    'Support': {de:'Unterstützen', es:'Apoyar', fr:'Soutenir'},
    'Close': {de:'Schließen', es:'Cerrar', fr:'Fermer'},
    'Primary': {de:'Hauptnavigation', es:'Navegación principal', fr:'Navigation principale'},
    'Grid': {de:'Raster', es:'Cuadrícula', fr:'Grille'},
    'List': {de:'Liste', es:'Lista', fr:'Liste'},
    'Getting started': {de:'Erste Schritte', es:'Primeros pasos', fr:'Bien démarrer'},
    'Status': {de:'Status', es:'Estado', fr:'Statut'},
    'Sort': {de:'Sortierung', es:'Ordenar', fr:'Tri'},
    '● Status · 🏷 Category · ↕ Sort · 🔎 Search': {
      de:'● Status · 🏷 Kategorie · ↕ Sortierung · 🔎 Suche',
      es:'● Estado · 🏷 Categoría · ↕ Ordenar · 🔎 Buscar',
      fr:'● Statut · 🏷 Catégorie · ↕ Tri · 🔎 Recherche'
    },

    'Useful Scriptable apps in one place': {
      de:'Nützliche Scriptable-Apps an einem Ort',
      es:'Aplicaciones útiles de Scriptable en un solo lugar',
      fr:'Des apps Scriptable utiles réunies au même endroit'
    },
    'Install our apps through the native .scriptable package. On iPhone, open the file in Scriptable and confirm the import; Scriptable handles an existing script during import.': {
      de:'Installiere unsere Apps direkt über das native .scriptable-Paket. Öffne die Datei auf dem iPhone in Scriptable und bestätige den Import; vorhandene Skripte behandelt Scriptable beim Import.',
      es:'Instala nuestras apps mediante el paquete nativo .scriptable. En el iPhone, abre el archivo en Scriptable y confirma la importación; Scriptable gestiona los scripts existentes durante la importación.',
      fr:'Installez nos apps avec le paquet natif .scriptable. Sur iPhone, ouvrez le fichier dans Scriptable et confirmez l’importation ; Scriptable gère les scripts existants pendant l’importation.'
    },
    'Other developers': {de:'Andere Entwickler', es:'Otros desarrolladores', fr:'Autres développeurs'},
    'Downloads are served directly from our site.': {
      de:'Downloads werden direkt von unserer Website bereitgestellt.',
      es:'Las descargas se sirven directamente desde nuestro sitio.',
      fr:'Les téléchargements sont servis directement depuis notre site.'
    },
    "Selected community projects. Installation fetches the original code directly from the author's repository and prepares it for Scriptable.": {
      de:'Ausgewählte Community-Projekte. Bei der Installation wird der Originalcode direkt aus dem Repository des Autors geladen und für Scriptable vorbereitet.',
      es:'Proyectos seleccionados de la comunidad. La instalación obtiene el código original directamente del repositorio del autor y lo prepara para Scriptable.',
      fr:'Projets communautaires sélectionnés. L’installation récupère le code original directement depuis le dépôt de l’auteur et le prépare pour Scriptable.'
    },
    'Category': {de:'Kategorie', es:'Categoría', fr:'Catégorie'},
    'Search': {de:'Suchen', es:'Buscar', fr:'Rechercher'},
    'Search projects…': {de:'Projekte suchen…', es:'Buscar proyectos…', fr:'Rechercher des projets…'},
    'Name A–Z': {de:'Name A–Z', es:'Nombre A–Z', fr:'Nom A–Z'},
    'Author A–Z': {de:'Autor A–Z', es:'Autor A–Z', fr:'Auteur A–Z'},
    'Variant': {de:'Variante', es:'Variante', fr:'Variante'},
    'active': {de:'aktiv', es:'activos', fr:'actifs'},
    'Clear filters': {de:'Filter löschen', es:'Borrar filtros', fr:'Effacer les filtres'},
    'Previous page': {de:'Vorherige Seite', es:'Página anterior', fr:'Page précédente'},
    'Next page': {de:'Nächste Seite', es:'Página siguiente', fr:'Page suivante'},
    'Checking': {de:'Wird geprüft', es:'Comprobando', fr:'Vérification'},
    'Last checked': {de:'Zuletzt geprüft', es:'Última comprobación', fr:'Dernière vérification'},
    'Online': {de:'Online', es:'En línea', fr:'En ligne'},
    'Offline': {de:'Offline', es:'Sin conexión', fr:'Hors ligne'},
    'ℹ️ These projects are not ours. During installation, the original code is fetched directly from the author and only wrapped in the .scriptable format; the script code itself is not modified. Review the original project and its setup/API requirements before running third-party code.': {
      de:'ℹ️ Diese Projekte stammen nicht von uns. Bei der Installation wird der Originalcode direkt vom Autor geladen und nur in das .scriptable-Format verpackt; der Skriptcode selbst wird nicht verändert. Prüfe vor dem Ausführen von Drittanbieter-Code das ursprüngliche Projekt sowie dessen Einrichtung und API-Anforderungen.',
      es:'ℹ️ Estos proyectos no son nuestros. Durante la instalación, el código original se obtiene directamente del autor y solo se empaqueta en formato .scriptable; el código del script no se modifica. Revisa el proyecto original y sus requisitos de configuración/API antes de ejecutar código de terceros.',
      fr:'ℹ️ Ces projets ne sont pas les nôtres. Pendant l’installation, le code original est récupéré directement auprès de l’auteur et uniquement empaqueté au format .scriptable ; le code du script n’est pas modifié. Consultez le projet d’origine ainsi que ses exigences de configuration/API avant d’exécuter du code tiers.'
    },
    'The community catalog is curated from public Scriptable projects and community recommendations.': {
      de:'Der Community-Katalog wird aus öffentlichen Scriptable-Projekten und Empfehlungen der Community zusammengestellt.',
      es:'El catálogo comunitario se selecciona a partir de proyectos públicos de Scriptable y recomendaciones de la comunidad.',
      fr:'Le catalogue communautaire est sélectionné à partir de projets Scriptable publics et de recommandations de la communauté.'
    },

    'SUPPORT THE PROJECT': {de:'PROJEKT UNTERSTÜTZEN', es:'APOYAR EL PROYECTO', fr:'SOUTENIR LE PROJET'},
    'Support further development.': {de:'Unterstütze die weitere Entwicklung.', es:'Apoya el desarrollo futuro.', fr:'Soutenez le développement futur.'},
    'If Scriptable Apps saves you time, you can support further development through Buy Me a Coffee.': {
      de:'Wenn dir Scriptable Apps Zeit spart, kannst du die weitere Entwicklung über Buy Me a Coffee unterstützen.',
      es:'Si Scriptable Apps te ahorra tiempo, puedes apoyar el desarrollo futuro mediante Buy Me a Coffee.',
      fr:'Si Scriptable Apps vous fait gagner du temps, vous pouvez soutenir son développement via Buy Me a Coffee.'
    },
    'Open Buy Me a Coffee': {de:'Buy Me a Coffee öffnen', es:'Abrir Buy Me a Coffee', fr:'Ouvrir Buy Me a Coffee'},

    'All': {de:'Alle', es:'Todos', fr:'Tous'},
    'Sport': {de:'Sport', es:'Deporte', fr:'Sport'},
    'Weather': {de:'Wetter', es:'Tiempo', fr:'Météo'},
    'News': {de:'Nachrichten', es:'Noticias', fr:'Actualités'},
    'Calendar': {de:'Kalender', es:'Calendario', fr:'Calendrier'},
    'Finance': {de:'Finanzen', es:'Finanzas', fr:'Finance'},
    'Space': {de:'Weltraum', es:'Espacio', fr:'Espace'},
    'Tools': {de:'Werkzeuge', es:'Herramientas', fr:'Outils'},
    'Reading': {de:'Lesen', es:'Lectura', fr:'Lecture'},
    'Cars': {de:'Autos', es:'Coches', fr:'Voitures'},
    'Gaming': {de:'Gaming', es:'Juegos', fr:'Jeux'},
    'Music': {de:'Musik', es:'Música', fr:'Musique'},
    'Social': {de:'Soziales', es:'Social', fr:'Réseaux sociaux'},
    'Mobile': {de:'Mobil', es:'Móvil', fr:'Mobile'},
    'Health': {de:'Gesundheit', es:'Salud', fr:'Santé'},
    'Travel': {de:'Reisen', es:'Viajes', fr:'Voyages'},
    'Design': {de:'Design', es:'Diseño', fr:'Design'},
    'Shopping': {de:'Einkaufen', es:'Compras', fr:'Shopping'},

    'Copying…': {de:'Wird kopiert…', es:'Copiando…', fr:'Copie…'},
    '✓ Code copied': {de:'✓ Code kopiert', es:'✓ Código copiado', fr:'✓ Code copié'},
    '⚠️ Copy failed': {de:'⚠️ Kopieren fehlgeschlagen', es:'⚠️ Error al copiar', fr:'⚠️ Échec de la copie'},
    'Preparing installation…': {de:'Installation wird vorbereitet…', es:'Preparando la instalación…', fr:'Préparation de l’installation…'},
    '✓ Opening in Scriptable': {de:'✓ Wird in Scriptable geöffnet', es:'✓ Abriendo en Scriptable', fr:'✓ Ouverture dans Scriptable'},
    '✓ Ready for Scriptable': {de:'✓ Bereit für Scriptable', es:'✓ Listo para Scriptable', fr:'✓ Prêt pour Scriptable'},
    '⚠️ Install failed – opening original': {de:'⚠️ Installation fehlgeschlagen – Original wird geöffnet', es:'⚠️ Error de instalación – abriendo el original', fr:'⚠️ Échec de l’installation – ouverture de l’original'},
    'Third-party': {de:'Drittanbieter', es:'De terceros', fr:'Tiers'},
    'Author': {de:'Autor', es:'Autor', fr:'Auteur'},
    '📲 Install': {de:'📲 Installieren', es:'📲 Instalar', fr:'📲 Installer'},
    '↗ Project': {de:'↗ Projekt', es:'↗ Proyecto', fr:'↗ Projet'},
    'projects': {de:'Projekte', es:'proyectos', fr:'projets'},
    'app': {de:'App', es:'aplicación', fr:'app'},
    'apps': {de:'Apps', es:'aplicaciones', fr:'apps'},
    'No results': {de:'Keine Ergebnisse', es:'Sin resultados', fr:'Aucun résultat'},
    'No projects matched this filter or search.': {
      de:'Keine Projekte entsprechen diesem Filter oder der Suche.',
      es:'Ningún proyecto coincide con este filtro o búsqueda.',
      fr:'Aucun projet ne correspond à ce filtre ou à cette recherche.'
    },

    'Skip to content': {de:'Zum Inhalt springen', es:'Saltar al contenido', fr:'Aller au contenu'},
    'Menu': {de:'Menü', es:'Menú', fr:'Menu'},
    'Mobile navigation': {de:'Mobile Navigation', es:'Navegación móvil', fr:'Navigation mobile'}
  };

  const SHARED = {
    website: {cs:'Web', en:'Website', de:'Website', es:'Sitio web', fr:'Site web'},
    credits: {cs:'Poděkování', en:'Credits', de:'Danksagungen', es:'Créditos', fr:'Crédits'},
    privacy: {cs:'Soukromí a cookies', en:'Privacy & Cookies', de:'Datenschutz & Cookies', es:'Privacidad y cookies', fr:'Confidentialité et cookies'},
    cookies: {cs:'Nastavení cookies', en:'Cookie settings', de:'Cookie-Einstellungen', es:'Configuración de cookies', fr:'Paramètres des cookies'},
    creditsTitle: {cs:'Poděkování a zdroje', en:'Credits & Acknowledgements', de:'Danksagungen & Quellen', es:'Créditos y agradecimientos', fr:'Crédits et remerciements'}
  };

  function normalizeLang(lang) {
    const code = String(lang || 'en').toLowerCase().slice(0,2);
    return ['cs','en','de','es','fr'].includes(code) ? code : 'en';
  }

  function translate(cs, en, lang) {
    const code = normalizeLang(lang);
    if (code === 'cs') return cs ?? en ?? '';
    if (code === 'en') return en ?? cs ?? '';

    const base = String(en ?? cs ?? '');
    const direct = TEXT[base]?.[code];
    if (direct) return direct;

    const page = base.match(/^Page (\d+) of (\d+) · (\d+) selected$/);
    if (page) {
      const [, current, total, count] = page;
      if (code === 'de') return `Seite ${current} von ${total} · ${count} ausgewählt`;
      if (code === 'es') return `Página ${current} de ${total} · ${count} seleccionados`;
      if (code === 'fr') return `Page ${current} sur ${total} · ${count} sélectionnés`;
    }

    return base;
  }

  function applyShared(lang) {
    const code = normalizeLang(lang || document.documentElement.lang);
    const value = key => SHARED[key]?.[code] || SHARED[key]?.en || '';

    document.querySelectorAll('a[href="https://caseycz.github.io/"]').forEach(el => { el.textContent = value('website'); });
    document.querySelectorAll('a[href="credits.html"]').forEach(el => {
      if (!el.querySelector('[data-cs]')) el.textContent = value('credits');
    });
    document.querySelectorAll('a[href="privacy.html"]').forEach(el => { el.textContent = value('privacy'); });
    document.querySelectorAll('[data-cookie-settings]').forEach(el => {
      el.textContent = value('cookies');
      el.setAttribute('aria-label', value('cookies'));
    });

    const skip = document.querySelector('.skip-link');
    if (skip) skip.textContent = translate('Přeskočit na obsah', 'Skip to content', code);

    const creditsTitle = document.querySelector('.credits-content .hero h1');
    if (creditsTitle) creditsTitle.textContent = value('creditsTitle');

    const mobileButton = document.getElementById('mobileMenuButton');
    if (mobileButton) mobileButton.setAttribute('aria-label', translate('Nabídka', 'Menu', code));
    const mobileNav = document.querySelector('.mobile-nav-links');
    if (mobileNav) mobileNav.setAttribute('aria-label', translate('Mobilní navigace', 'Mobile navigation', code));
  }

  window.ScriptableI18n = Object.freeze({ translate, applyShared });

  const syncShared = () => applyShared(document.documentElement.lang);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', syncShared, {once:true});
  else syncShared();

  new MutationObserver(mutations => {
    if (mutations.some(m => m.type === 'attributes' && m.attributeName === 'lang')) syncShared();
  }).observe(document.documentElement, {attributes:true, attributeFilter:['lang']});
})();
