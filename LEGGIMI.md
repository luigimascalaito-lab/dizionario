# Dizionario Poetico Italiano ⇄ Romagnolo — app installabile

File da pubblicare insieme, nella stessa cartella (es. repository GitHub Pages `dizionario`):

- `index.html` (dati incorporati)
- `manifest.webmanifest`
- `sw.js`
- `icons/` (icon-192.png, icon-512.png, icon-maskable-512.png, apple-touch-icon.png)
- `dizionario.json` (facoltativo: l'app usa comunque la copia incorporata)

## Installazione
- **Android/Chrome, desktop Chrome/Edge:** compare il pulsante «Installa l’app» nell'intestazione (oppure l'icona di installazione nella barra degli indirizzi).
- **iPhone/iPad (Safari):** Condividi → Aggiungi alla schermata Home (l'app mostra il promemoria).

L'installazione richiede HTTPS (GitHub Pages va bene) o `localhost`; aperta da `file://` l'app funziona ma non si installa.

## Aggiornamenti
Il service worker usa «rete prima, cache come ripiego»: con connessione si vede sempre l'edizione nuova, senza connessione si usa l'ultima copia salvata. Per forzare il rinnovo della cache a ogni edizione, cambiare `VERSIONE` in `sw.js`.
