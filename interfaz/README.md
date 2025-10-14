
# Interfaz — Asistente VuelaConNosotros (UI)

Este directorio contiene la interfaz web (UI) basada en Streamlit que permite a un usuario conversar con el agente "Asistente VuelaConNosotros" a través del endpoint `/chat` expuesto por el servicio `agente_vcn`.

Resumen rápido
- `main.py` — Aplicación Streamlit que actúa como cliente web: captura entradas de usuario y envía POST JSON al endpoint `/chat` del agente. Muestra únicamente el campo `output` de la respuesta del agente y soporta un efecto de streaming local para la respuesta.
- `pyproject.toml` — Metadatos del paquete y dependencias mínimas: `streamlit` y requerimiento de Python >= 3.12.

Objetivo

Proveer una interfaz simple y segura en español para interactuar con el agente conversacional. La UI está pensada para desarrollo y pruebas locales; no implementa autenticación ni persistencia fuera de la sesión de Streamlit.

Componentes

- `main.py`
	- Carga configuración desde la variable de entorno `CHAT_URL` o desde `st.secrets`.
	- Por defecto envía las peticiones a `http://localhost:8001/chat` si no se configura nada.
	- Envía POST JSON con la forma {"message": "tu mensaje"} y maneja respuestas JSON esperando el campo `output`.
	- Mantiene el historial de la conversación en `st.session_state.messages`.

Flujo (alto nivel)

1. El usuario escribe un mensaje en la caja de chat de Streamlit.
2. La UI envía POST al `CHAT_URL` con payload JSON {"message": "..."}.
3. La UI muestra la respuesta final usando exclusivamente el campo `output` de la respuesta JSON; si falta `output`, intenta extraer texto útil de `raw_responses` o muestra un error legible.

Configuración y variables de entorno

- `CHAT_URL` — URL del endpoint `/chat` al que la interfaz enviará mensajes. Si no se especifica, la app usa `http://localhost:8001/chat`.
	- Ejemplo: `CHAT_URL=http://127.0.0.1:8001/chat`
- Alternativa segura: colocar `CHAT_URL` en `st.secrets` (archivo `secrets.toml` de Streamlit) para no exponerla en el entorno.

Dependencias

Declaradas en `pyproject.toml`:

- Python >= 3.12
- streamlit >= 1.50.0

Instalación y ejecución local (recomendado)

La base de ejecución en este repositorio utiliza `uv` (Astral) para sincronizar dependencias y ejecutar procesos de forma reproducible

Pasos rápidos (PowerShell)

1. Abrir una terminal en la carpeta `interfaz`.

2. Sincronizar dependencias en el entorno gestionado por `uv`:

```powershell
# sincroniza las dependencias declaradas (crea/actualiza el entorno administrado por uv)
uv sync --frozen --no-dev
```

3. Ejecutar la aplicación Streamlit usando `uv run`:

```powershell
# ejecuta Streamlit con el main.py; cambia --server.port si ya hay otra app en 8501
uv run streamlit run main.py -- --server.port 8501
```

Notas:
- El doble `--` separa los argumentos de `uv run` de los argumentos del comando `streamlit`.
- Si prefieres no usar `uv`, puedes crear un entorno virtual estándar e instalar `streamlit` con `pip`.

Ejemplo alternativo sin `uv` (PowerShell)

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # si creas requirements.txt con streamlit
streamlit run main.py --server.port 8501
```

Pruebas rápidas

- Desde la interfaz: abrir el navegador en `http://localhost:8501` (o el puerto que hayas elegido) y chatear.
- Verificar que el backend del agente esté arriba (por defecto `agente_vcn` en `http://127.0.0.1:8001/chat`). Puedes probar con curl o PowerShell Invoke-RestMethod:

```powershell
curl -X POST http://127.0.0.1:8001/chat -H "Content-Type: application/json" -d '{"message":"Hola, quiero consultar un vuelo"}'

# o en PowerShell moderno
Invoke-RestMethod -Uri http://127.0.0.1:8001/chat -Method POST -ContentType 'application/json' -Body '{"message":"Hola"}'
```

Notas de diseño y recomendaciones

- La UI muestra únicamente el campo `output` de la respuesta del agente. Esto evita exponer estructuras internas del agente al usuario final.
- La interfaz no gestiona sesiones multi-usuario separadas; Streamlit mantiene estado en memoria por usuario-conexión. Para producción se recomienda añadir autenticación y una capa que identifique usuarios y persista historiales.
- Si el backend tiene latencia o streams largos, la UI emula un streaming local a partir del texto devuelto por el endpoint.

Integración con `agente_vcn`

- Asegúrate de que `agente_vcn` esté ejecutándose y disponible en la URL configurada en `CHAT_URL` (por defecto `http://localhost:8001/chat`).
- Si necesitas cambiar el puerto del agente o host, actualiza `CHAT_URL` en el entorno o en `st.secrets`.

Desarrollo y contribuciones

- Documenta cambios en la forma en que la UI consume el endpoint `/chat` (por ejemplo si cambias la estructura de la respuesta JSON).
- Añade pruebas o validaciones si amplías la lógica de extracción del campo `output` o del fallback desde `raw_responses`.

Licencia

Consulta la raíz del repositorio para la licencia principal.

Contacto

Si necesitas ayuda para levantar la interfaz o integrarla con `agente_vcn`, abre un issue en el repositorio.

