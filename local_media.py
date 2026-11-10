"""Servicios locales de imagen y vídeo para AI Music Video Studio.
ComfyUI debe estar en localhost:8188 con un checkpoint descargado por el usuario.
FFmpeg debe estar instalado localmente y accesible en PATH.
"""
import json
import os
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

COMFY_BASE = os.environ.get("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
MAX_WEBM_BYTES = 500 * 1024 * 1024


class MediaError(RuntimeError):
    pass


def request_comfy(path, data=None, timeout=20):
    url = COMFY_BASE + path
    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data is not None else None,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except urllib.error.URLError as exc:
        raise MediaError(
            "ComfyUI no responde. Abre ComfyUI localmente y comprueba que usa el puerto 8188. "
            + str(exc)
        ) from exc


def comfy_status():
    information = request_comfy("/object_info/CheckpointLoaderSimple")
    inputs = information["CheckpointLoaderSimple"]["input"]["required"]
    choices = inputs["ckpt_name"][0]
    names = list(choices) if isinstance(choices, list) else []
    if not names:
        raise MediaError("No hay checkpoints. Descarga un modelo compatible y colócalo en ComfyUI/models/checkpoints.")
    return {"available": True, "models": names, "selected": os.environ.get("COMFY_CHECKPOINT", names[0])}


def _workflow(checkpoint, positive, negative, width, height, seed):
    # Nodos estándar de ComfyUI; sin dependencias de custom nodes.
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": checkpoint}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": positive, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": negative, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": 22, "cfg": 7.0, "sampler_name": "euler",
            "scheduler": "normal", "denoise": 1,
            "model": ["1", 0], "positive": ["2", 0],
            "negative": ["3", 0], "latent_image": ["4", 0],
        }},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "AI_Music_Video_Studio", "images": ["6", 0]}},
    }


def generate_image(visual, style="infantil", checkpoint=None, width=768, height=432, seed=None):
    if not isinstance(visual, str) or not visual.strip():
        raise MediaError("La escena necesita una descripción visual.")
    status = comfy_status()
    checkpoint = checkpoint or status["selected"]
    if checkpoint not in status["models"]:
        raise MediaError("Modelo no encontrado en ComfyUI: " + checkpoint)
    width, height = int(width), int(height)
    if not (256 <= width <= 1536 and 256 <= height <= 1536 and width % 8 == 0 and height % 8 == 0):
        raise MediaError("Resolución no válida para ComfyUI.")
    seed = int(seed) if seed is not None else int.from_bytes(os.urandom(6), "little")
    styles = {
        "infantil": "beautiful colorful children's picture book illustration, soft pencil and watercolor, friendly expressive characters",
        "navidad": "magical Christmas children's storybook illustration, warm holiday lights, snowy night",
        "anime": "anime illustration, clean lineart, dynamic composition",
        "pop": "vibrant pop art music video illustration, modern colorful composition",
        "cinematico": "cinematic digital painting, dramatic lighting, atmospheric depth of field",
    }
    positive = (styles.get(style, styles["infantil"]) + ". " + visual.strip())[:1800]
    negative = "watermark, logo, words, letters, captions, low quality, distorted hands, extra limbs"
    workflow = _workflow(checkpoint, positive, negative, width, height, seed)
    data = request_comfy("/prompt", {"prompt": workflow, "client_id": str(uuid.uuid4())})
    prompt_id = data.get("prompt_id")
    if not prompt_id:
        raise MediaError("ComfyUI rechazó el flujo. " + json.dumps(data, ensure_ascii=False)[:600])
    until = time.monotonic() + 600
    while time.monotonic() < until:
        history = request_comfy("/history/" + urllib.parse.quote(prompt_id), timeout=30)
        result = history.get(prompt_id)
        if result:
            status_obj = result.get("status", {})
            if status_obj.get("status_str") == "error":
                raise MediaError("ComfyUI falló al crear la imagen; revisa su consola.")
            for output in result.get("outputs", {}).values():
                for img in output.get("images", []):
                    query = urllib.parse.urlencode({
                        "filename": img["filename"],
                        "subfolder": img.get("subfolder", ""),
                        "type": img.get("type", "output"),
                    })
                    return COMFY_BASE + "/view?" + query
        time.sleep(1.5)
    raise MediaError("ComfyUI tardó más de 10 minutos. Prueba otro modelo o menor resolución.")


def fetch_generated_image(image_url):
    # No aceptamos URLs arbitrarias: solo la ruta /view del propio ComfyUI local.
    parsed = urllib.parse.urlparse(image_url)
    base = urllib.parse.urlparse(COMFY_BASE)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc or parsed.path != "/view":
        raise MediaError("URL de imagen no autorizada.")
    with urllib.request.urlopen(image_url, timeout=60) as response:
        data = response.read(20 * 1024 * 1024 + 1)
        mime = response.headers.get("Content-Type", "image/png")
    if len(data) > 20 * 1024 * 1024:
        raise MediaError("La imagen supera los 20 MB.")
    if not mime.startswith("image/"):
        raise MediaError("ComfyUI no devolvió una imagen.")
    return data, mime


def convert_webm_to_mp4(webm):
    ffmpeg = os.environ.get("FFMPEG_PATH") or shutil.which("ffmpeg")
    if not ffmpeg:
        raise MediaError("Falta FFmpeg. Instálalo y añádelo a PATH para exportar en MP4.")
    if not 0 < len(webm) <= MAX_WEBM_BYTES:
        raise MediaError("Vídeo vacío o superior a 500 MB.")
    with tempfile.TemporaryDirectory(prefix="music_video_") as folder:
        source = Path(folder) / "input.webm"
        target = Path(folder) / "output.mp4"
        source.write_bytes(webm)
        command = [
            ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(source),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
            "-movflags", "+faststart", str(target),
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=1800, check=False)
        except subprocess.TimeoutExpired as exc:
            raise MediaError("La conversión MP4 superó los 30 minutos.") from exc
        if result.returncode != 0 or not target.is_file():
            raise MediaError("FFmpeg no pudo crear MP4: " + result.stderr[-1200:])
        return target.read_bytes()
