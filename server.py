"""Servidor local, sin servicios de pago: Whisper para audio y Ollama para storyboard."""
from email.parser import BytesParser
from email.policy import default
import json
import os
import tempfile
import urllib.request
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")


def transcribe(path):
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise RuntimeError("Falta faster-whisper. Ejecuta INSTALAR_WINDOWS.bat para instalarlo.") from e
    device = os.environ.get("WHISPER_DEVICE", "cpu")
    size = os.environ.get("WHISPER_MODEL", "small")
    try:
        model = WhisperModel(size, device=device, compute_type="float16" if device == "cuda" else "int8")
    except Exception as e:
        if device == "cuda":
            raise RuntimeError("Error CUDA: prueba configurar WHISPER_DEVICE=cpu. " + str(e))
        raise
    segments, _ = model.transcribe(path, beam_size=5, vad_filter=False, task="transcribe")
    entries = [{"start": round(z.start, 2), "end": round(z.end, 2), "text": z.text.strip()} for z in segments if z.text.strip()]
    if not entries:
        raise RuntimeError("Whisper no detectó palabras; revisa que el archivo contenga voz.")
    return entries


def fallback_storyboard(entries):
    out = []
    for x in entries:
        t = x["text"]
        duration = max(3, x["end"] - x["start"])
        out.append({"text": t, "seconds": round(duration, 2), "visual": "Ilustrar de manera narrativa: " + t})
    return out[:120]


def generate_storyboard(entries, style):
    lyrics = "\n".join(f"[{x['start']:.1f}-{x['end']:.1f}s] {x['text']}" for x in entries)
    payload = {
        "model": MODEL,
        "stream": False,
        "format": "json",
        "prompt": (
            'Eres director de videoclips. Devuelve SOLO JSON valido con esta forma: '
            '{"scenes":[{"text":"fragmento de letra", "visual":"descripcion concreta de ilustracion con personajes y escenario", "seconds":8}]}.'
            "Genera escenas que narren literalmente lo que sucede en la cancion, preserva personajes entre escenas, "
            "sin inventar nombres. Una escena por segmento o agrupacion corta, maximo 50 escenas. "
            f"Estilo visual: {style}. Segmentos transcritos:\n{lyrics[:14000]}"
        )
    }
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        json.dumps(payload).encode(),
        {"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=420) as res:
            obj = json.loads(json.load(res)["response"])
        scenes = obj.get("scenes", [])
        cleaned = [
            {
                "text": str(s.get("text", ""))[:400],
                "visual": str(s.get("visual", ""))[:800],
                "seconds": max(1, min(30, float(s.get("seconds", 8)))),
            }
            for s in scenes
            if isinstance(s, dict)
        ]
        if not cleaned:
            raise ValueError("Ollama devolvió storyboard vacío")
        return cleaned, "Ollama + Whisper"
    except Exception:
        return fallback_storyboard(entries), "Whisper; storyboard básico (Ollama no disponible)"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        data = (ROOT / "index.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/api/automatico":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size < 150_000_000:
                raise ValueError("El archivo debe medir menos de 150 MB.")
            content_type = self.headers.get("Content-Type", "")
            if not content_type.lower().startswith("multipart/form-data"):
                raise ValueError("Solicitud inválida: se esperaba multipart/form-data.")
            body = self.rfile.read(size)
            message = BytesParser(policy=default).parsebytes(
                b"MIME-Version: 1.0\r\nContent-Type: " + content_type.encode("ascii") + b"\r\n\r\n" + body
            )
            upload = next((p for p in message.iter_parts() if p.get_param("name", header="content-disposition") == "audio"), None)
            if upload is None:
                raise ValueError("Falta el archivo de audio.")
            filename = os.path.basename(upload.get_filename() or "cancion.mp3")
            suffix = Path(filename).suffix.lower()
            if suffix not in (".mp3", ".wav", ".m4a", ".flac", ".ogg", ".webm"):
                raise ValueError("Usa MP3, WAV, M4A, FLAC, OGG o WebM.")
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
                path = f.name
                f.write(upload.get_payload(decode=True))
            try:
                entries = transcribe(path)
            finally:
                os.unlink(path)
            scenes, mode = generate_storyboard(entries, "ilustración narrativa infantil o el estilo seleccionado en la web")
            result = {
                "lyrics": "\n".join(x["text"] for x in entries),
                "scenes": scenes,
                "segments": entries,
                "mode": mode,
            }
            self.send_json(result, 200)
        except Exception as e:
            self.send_json({"error": str(e)}, 400)

    def send_json(self, obj, code):
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print("Abre http://127.0.0.1:8765 en Chrome o Edge")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
