# AI Music Video Studio V2 — motor automático local experimental

## ¿Qué funciona ahora?
- **Extracción automática de letra desde un MP3** mediante faster-whisper local.
- **Generación automática de storyboard con Ollama**, si está instalado y se ha descargado `llama3.2:3b`. Cuando Ollama no responde se crea un storyboard básico por segmentos transcritos.
- Editor manual de letra y escenas; imágenes propias; zoom, desplazamientos, previsualización con audio y exportación WebM.
- Sin pagos por API ni límites de créditos. Los modelos son gratuitos y corren en tu ordenador.

## Instalación en Windows
1. Instala Python 3.11 o 3.12 y marca «Add to PATH».
2. Ejecuta `INSTALAR_WINDOWS.bat` (requiere internet la primera vez).
3. Instala Ollama desde https://ollama.com/download y ejecuta `ollama pull llama3.2:3b` en terminal.
4. Ejecuta `INICIAR_WINDOWS.bat` y abre http://127.0.0.1:8765.
5. Selecciona MP3 y haz clic en «Extraer letra y crear storyboard con IA».

## Limitaciones transparentes
- **La IA aún no genera imágenes automáticamente**: el storyboard incluye descripciones visuales editables y la aplicación permite añadir imágenes. Próxima integración: ComfyUI local.
- **Whisper es imperfecto con voces cantadas**, coros, música fuerte y nombres propios: comprueba la transcripción.
- El reconocimiento es CPU por defecto para mayor compatibilidad; si tienes CUDA y cuDNN correctamente configurados, puedes configurar `WHISPER_DEVICE=cuda` antes de iniciar para acelerarlo.
- La versión V2 aún NO asegura la sincronización exacta por palabra: las duraciones de las escenas se ajustan a la duración completa del audio.
- La salida es WebM, no MP4. No hace lip-sync ni vídeo IA real.
- Ollama no se incluye dentro del ZIP: es un instalador independiente y requiere descargar un modelo.
- La primera ejecución de Whisper descarga su modelo de Internet; después se ejecuta localmente.
- No subas canciones protegidas si no cuentas con los derechos adecuados para reutilizarlas.

## Seguridad
Servidor ligado exclusivamente a `127.0.0.1`, sin exponerlo a Internet. Los archivos de audio se procesan localmente y se eliminan del directorio temporal tras transcribirlos.