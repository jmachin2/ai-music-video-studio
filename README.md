# AI Music Video Studio · Windows (versión 0.3 experimental)

Aplicación de escritorio para Windows con interfaz propia, basada en la V2. Gratuita, sin cuentas ni créditos por generación. Todo el procesamiento del audio se realiza localmente; los modelos se descargan la primera vez.

## Instalar y abrir en Windows

1. Instala **Python 3.12 de 64 bits** (marca *Add Python to PATH*). Necesitas Windows con Microsoft Edge WebView2 Runtime; suele venir instalado con Windows 10/11.
2. Descarga el repositorio como ZIP y descomprímelo en una carpeta normal (no lo ejecutes dentro del ZIP).
3. Ejecuta `INSTALAR_WINDOWS.bat` una sola vez; instalará las librerías en `.venv`.
4. Para crear el storyboard automáticamente con IA, instala Ollama desde https://ollama.com/download y ejecuta `ollama pull llama3.2:3b` en una consola. Déjalo funcionando.
5. Haz doble clic en `ABRIR_APLICACION_WINDOWS.bat`: se abrirá una ventana independiente, sin navegador visible.
6. Importa un MP3 y pulsa **Extraer letra y crear storyboard con IA**.

**Alternativa:** `INICIAR_WINDOWS.bat` permite abrir la versión en navegador en `http://127.0.0.1:8765`.

**Crear EXE en Windows:** ejecuta `CREAR_EXE_WINDOWS.bat`. Es una compilación *onedir* con PyInstaller: la carpeta completa de `dist/AI-Music-Video-Studio/` constituye la distribución; el `.exe` no contiene Ollama ni los modelos Whisper. No se ha compilado ni probado en Windows desde este entorno.

## Funciones reales de esta versión

- Carga de audio local, transcripción **experimental** con faster-whisper y preparación de storyboard con Ollama.
- Si Ollama no está disponible, storyboard simplificado a partir de los fragmentos reconocidos.
- Editor de texto y de escenas, imágenes añadidas manualmente, movimientos de cámara, previsualización y exportación **WebM** con audio.
- Servidor HTTP limitado al equipo local (`127.0.0.1`), con puerto aleatorio cuando se utiliza la aplicación de escritorio.

## Pendiente para siguientes versiones

- Generación automática de imágenes con ComfyUI en tu NVIDIA.
- Exportación directa a MP4 y sincronización avanzada por frase.
- Instalador de Windows de un solo clic, firmado y probado en Windows.

## Limitaciones

- Las canciones cantadas, coros y nombres propios pueden transcribirse mal. Revisa la letra.
- La GPU NVIDIA no se aprovecha automáticamente en Whisper: por defecto se ejecuta en CPU. El modo CUDA exige librerías CUDA/cuDNN compatibles.
- La ventana de escritorio usa Microsoft Edge WebView2. Si tu Windows no lo incluye, instálalo desde Microsoft.
- No publiques canciones, contraseñas ni modelos pesados en GitHub. Nunca se necesitan claves de API de pago.
- El archivo MP3 se procesa localmente y el temporal se elimina tras la transcripción.
