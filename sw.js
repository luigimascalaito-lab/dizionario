/* Service worker del Dizionèri — funzionamento offline
   Strategia:
   - App shell (index.html, icone, manifest): cache-first con aggiornamento in background.
   - dizionario.json: network-first (così gli aggiornamenti arrivano subito),
     con fallback alla copia in cache quando si è offline.
   Per pubblicare una nuova versione dell'app basta incrementare VERSION. */

const VERSION = 'v1';
const CACHE = 'dizioneri-' + VERSION;

const SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png',
  './dizionario.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;

  // dizionario.json: prima la rete, poi la cache
  if (url.pathname.endsWith('dizionario.json')) {
    e.respondWith(
      fetch(e.request)
        .then((r) => {
          const copia = r.clone();
          caches.open(CACHE).then((c) => c.put(e.request, copia));
          return r;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // tutto il resto (app shell): prima la cache, poi la rete
  e.respondWith(
    caches.match(e.request).then((hit) => {
      const rete = fetch(e.request)
        .then((r) => {
          if (r && r.ok) {
            const copia = r.clone();
            caches.open(CACHE).then((c) => c.put(e.request, copia));
          }
          return r;
        })
        .catch(() => hit);
      return hit || rete;
    })
  );
});
