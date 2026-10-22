// Service worker del Dizionario. Aumentare VERSIONE a ogni nuova edizione.
const VERSIONE = 'dizionario-v2';
const BASE_FILES = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSIONE).then(c => c.addAll(BASE_FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSIONE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// Rete prima, cache come ripiego: con la connessione si vede sempre l'edizione aggiornata, senza connessione l'app funziona comunque.
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET' || new URL(r.url).origin !== location.origin) return;
  e.respondWith(
    fetch(r).then(resp => {
      if (resp && resp.ok) { const copia = resp.clone(); caches.open(VERSIONE).then(c => c.put(r, copia)); }
      return resp;
    }).catch(() => caches.match(r).then(m => m || (r.mode === 'navigate' ? caches.match('./index.html') : undefined)))
  );
});
