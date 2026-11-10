# AI Music Video Studio · Windows (versión 0.4, experimental)

**Objetivo:** programa de escritorio para Windows que transforme una canción MP3 en un videoclip animado, utilizando únicamente herramientas gratuitas ejecutadas en el ordenador. No se requieren suscripciones ni servicios de IA de pago.

## Estado real

- **Interfaz Windows:** incorporada mediante pywebview (WebView2), pendiente de prueba en Windows real.
- **Letra automática:** faster-whisper local, experimental con voz cantada.
- **Storyboard automático:** Ollama local con modelo llama3.2:3b. Si no responde, se usa un storyboard básico.
- **Ilustraciones IA:** integración nueva con la API local de ComfyUI (modelos tipo Stable Diffusion con nodos básicos). Hay botones por escena y para generar las imágenes pendientes. El modelo no está incluido.
- **Vídeo:** editor con movimientos de cámara y exportación MP4 mediante grabación WebM + conversión local con FFmpeg. No es exportación rápida: requiere reproducir el audio entero.
- **Instalador .exe:** flujo de compilación Windows con PyInstaller + Inno Setup en GitHub Actions. La compilación y el instalador no se han validado todavía.

## Instalación de desarrollo en Windows 10/11

1. Instala Python 3.12 (64 bits) y el runtime Microsoft Edge WebView2.
2. Descomprime el repositorio. Ejecuta `INSTALAR_WINDOWS.bat` una vez.
3. Ejecuta `ABRIR_APLICACION_WINDOWS.bat`. Se abrirá la aplicación en una ventana de escritorio.
4. Instala Ollama en Windows, descarga el modelo con `ollama pull llama3.2:3b` y mantenlo abierto.
5. Instala ComfyUI localmente con un modelo compatible de Stable Diffusion en `ComfyUI/models/checkpoints`. Inicia ComfyUI en `http://127.0.0.1:8188`. En la aplicación pulsa **Comprobar ComfyUI**.
6. Instala FFmpeg y añádelo al PATH de Windows para exportar MP4.
7. Sube una canción, extrae letra y storyboard, genera ilustraciones y exporta.

**Advertencia:** no hay un asistente que instale Ollama, ComfyUI, los modelos y FFmpeg automáticamente. El instalador del programa no incluye estos componentes grandes. La descarga inicial de los modelos necesita internet; después el procesamiento es local.

## Generación del instalador desde GitHub

Se añadió `.github/workflows/windows-installer.yml`. En la pestaña **Actions** del repositorio, busca **Windows desktop installer** y ejecuta **Run workflow**. Si finaliza correctamente, descarga el artefacto **AI-Music-Video-Studio-Windows-Installer**, que contiene el instalador de Windows.

Para compilarlo en un PC Windows: `CREAR_EXE_WINDOWS.bat` genera la carpeta de programa con PyInstaller. `installer.iss` se utiliza con Inno Setup 6 para construir el instalador.

**Limitaciones conocidas**

- Whisper puede equivocarse con canciones, coros y nombres propios: revisa la transcripción.
- La consistencia de personajes entre varias escenas **no está resuelta** todavía; generar imágenes por descripción puede cambiar el aspecto de los personajes.
- La secuencia del storyboard se reparte por duración relativa, **sin alineación exacta de cada frase**.
- ComfyUI necesita una GPU/modelo compatibles; checkpoints SDXL, SD 1.5 u otros pueden variar en memoria y resultados. Un workflow clásico no sirve para todos los tipos de modelo (por ejemplo FLUX).
- La exportación MP4 usa la grabación de canvas del motor WebView2; es necesario comprobar que MediaRecorder y captureStream están disponibles en el equipo.
- GitHub es solo el repositorio: la aplicación y los motores de IA se ejecutan en Windows. El repositorio actual es público; no subas canciones ni archivos personales.
- El servidor escucha únicamente en `127.0.0.1`, no en internet.
