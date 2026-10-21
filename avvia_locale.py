#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Avviatore locale del dizionario.

Serve la cartella in cui risiede tramite un piccolo server HTTP e apre il
browser su index.html: in questo modo la pagina viene caricata da
http://localhost e può leggere il file esterno dizionario.json, cosa che il
protocollo file:// (doppio clic) non consente.

Uso:  python3 avvia_locale.py          (dalla cartella con index.html e dizionario.json)
      oppure doppio clic sul file, se Python è associato ai .py
Arresto: Ctrl+C nella finestra del terminale.
"""
import http.server, socketserver, webbrowser, os, sys, threading

cartella = os.path.dirname(os.path.abspath(__file__))
os.chdir(cartella)
if not os.path.exists('index.html') and not os.path.exists('dizioneri_romagnolo.html'):
    sys.exit("Metti questo script nella cartella che contiene index.html (e dizionario.json).")
pagina = 'index.html' if os.path.exists('index.html') else 'dizioneri_romagnolo.html'
if not os.path.exists('dizionario.json'):
    print("AVVISO: dizionario.json non è presente nella cartella; la pagina userà la copia incorporata.")

class Gestore(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')   # niente cache: gli aggiornamenti si vedono subito
        super().end_headers()
    def log_message(self, *a): pass

PORTA = 8000
while True:
    try:
        server = socketserver.TCPServer(("127.0.0.1", PORTA), Gestore)
        break
    except OSError:
        PORTA += 1
url = f"http://localhost:{PORTA}/{pagina}"
print(f"Dizionario in ascolto su {url}  (Ctrl+C per arrestare)")
threading.Timer(0.6, lambda: webbrowser.open(url)).start()
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer arrestato.")
