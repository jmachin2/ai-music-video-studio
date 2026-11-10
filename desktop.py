"""AI Music Video Studio - ventana de Windows, servidor solo local."""
from __future__ import annotations
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
import webview
import server

def main():
    if getattr(sys, "frozen", False):
        server.ROOT = Path(sys._MEIPASS)
    else:
        server.ROOT = Path(__file__).resolve().parent
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    httpd.daemon_threads = True
    worker = threading.Thread(target=httpd.serve_forever, daemon=True)
    worker.start()
    try:
        webview.create_window("AI Music Video Studio · Windows", f"http://127.0.0.1:{httpd.server_port}/", width=1360, height=850, min_size=(980, 640), background_color="#0b1020")
        webview.start(gui="edgechromium", debug=False)
    finally:
        httpd.shutdown()
        httpd.server_close()

if __name__ == "__main__":
    main()
