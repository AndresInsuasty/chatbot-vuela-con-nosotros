
# Agente VuelaConNosotros

Este directorio contiene el servicio HTTP que expone un agente conversacional (Asistente VuelaConNosotros) orientado a la gestión de incidencias por vuelos cancelados y la interacción con un servidor MCP (Model Context Protocol) para consultar y modificar reservas.

Resumen rápido
- `main.py` — Define una aplicación FastAPI con un endpoint `/chat` que recibe JSON `{message: str}` y devuelve la respuesta del agente junto con un resumen de las respuestas crudas y los nuevos ítems generados.
- `prompt.txt` — Instrucciones detalladas y reglas de seguridad que guían el comportamiento del agente (en español). Contiene el flujo obligatorio de verificación, manejo de vuelos cancelados, petición de `id_pasajero`, opciones de reagendamiento, plantillas y protección contra prompt injection.
- `pyproject.toml` — Metadatos del paquete y dependencias mínimas: `fastapi`, `uvicorn`, `openai-agents`, `python-dotenv`.

Objetivo

El agente actúa como un intermediario conversacional en español que:

- Recibe mensajes de usuario por POST JSON en `/chat`.
- Mantiene estado de sesión en memoria para conversaciones multi-turno (usa `OpenAIConversationsSession`).
- Consulta herramientas externas MCP (por ejemplo el microservicio contenido en `mcp_vcn`) para obtener estado de vuelo, opciones y gestionar reservas.

Componentes

- `main.py`: arranca la aplicación FastAPI y crea los objetos compartidos:
	- `MCPServerStreamableHttp` (configurado mediante la variable `MCP_SERVER_URL` o por defecto `http://127.0.0.1:8000/mcp`) como cliente de herramientas MCP.
	- `Agent` (de `openai-agents` o similar) con las instrucciones cargadas desde `prompt.txt`.
	- `OpenAIConversationsSession` para mantener el historial entre llamadas.

- `prompt.txt`: reglas y flujo que debe seguir el agente (seguridad, verificación, manejo de reembolso, NPS, etc.).

API

POST /chat
- Request JSON: {"message": "..."}
- Response JSON de ejemplo:

	{
		"output": "Texto de salida final del agente",
		"last_agent": "Asistente VuelaConNosotros",
		"last_response_id": "...",
		"raw_responses": [ {"response_id": "...", "output": "..."}, ... ],
		"new_items": [ {"type": "...", "repr": "..."}, ... ]
	}

Nota: El endpoint comparte la misma sesión en memoria mientras la aplicación esté en ejecución. Para mantener aislamiento entre usuarios o persistencia fuera del proceso sería necesario añadir gestión de sesiones/identificadores y una capa de almacenamiento.

Configuración y variables de entorno
- `MCP_SERVER_URL`: URL del servidor MCP al que el agente hará las llamadas (por defecto `http://127.0.0.1:8000/mcp`).
- Cualquier variable requerida por las bibliotecas subyacentes (por ejemplo claves de OpenAI) pueden cargarse mediante un archivo `.env` y `python-dotenv`.

Dependencias

Las dependencias principales se declaran en `pyproject.toml`:

- fastapi >= 0.119.0
- uvicorn >= 0.37.0
- openai-agents >= 0.3.3
- python-dotenv >= 1.1.1

Instalación y ejecución local (recomendado para desarrollo)

1. Abrir una terminal en la carpeta `agente_vcn`.
2. Crear un entorno virtual (opcional) e instalar dependencias:

```powershell
# sincroniza las dependencias declaradas (crea un entorno aislado gestionado por uv)
uv sync --frozen --no-dev
```

3. Exportar/crear un `.env` con cualquier credencial necesaria (por ejemplo, claves de proveedor de LLM) y, si usa un MCP local, asegúrese de que el servicio `mcp_vcn` esté corriendo en `MCP_SERVER_URL`.
ejemplo de .env

```powershell
OPENAI_API_KEY=sk-...
URL_MCP=http://127.0.0.1:8000/mcp
```

4. Ejecutar la aplicación:

```powershell
# ejecutar el main.py usando el entorno sincronizado
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

Pruebas rápidas

- Llamar al endpoint desde curl/HTTP client:

```powershell
curl -X POST http://127.0.0.1:8001/chat -H "Content-Type: application/json" -d '{"message":"Hola, quiero consultar un vuelo"}'
```

Integración con `mcp_vcn`

El agente está pensado para integrarse con el microservicio MCP (`mcp_vcn`) que expone herramientas como `estado_vuelo`, `opciones_vuelo`, `reservar_vuelo`, `eliminar_reserva_vuelo`. Para que el agente pueda usar estas herramientas:

1. Inicie el servicio MCP (directorio `mcp_vcn`) siguiendo sus instrucciones (por defecto escucha en http://127.0.0.1:8000/mcp).
2. Asegúrese de que `MCP_SERVER_URL` apunte a la URL correcta.

Notas de diseño y recomendaciones

- Seguridad: `prompt.txt` contiene protecciones contra prompt injection y reglas que deben prevalecer. No modifique el prompt sin una revisión de seguridad.
- Sesiones: Hoy la sesión se mantiene en memoria (`OpenAIConversationsSession`). Para producción, añadir identificación de sesiones y almacenamiento persistente.
- Manejo de errores: `main.py` transforma la salida del agente en un resumen serializable y captura excepciones de inicialización o ejecución, devolviendo errores 5xx cuando corresponde.

Desarrollo y contribuciones

- Respete las reglas del prompt y agregue pruebas unitarias para cualquier cambio que afecte la lógica del agente.
- Si añade nuevas herramientas MCP, actualice tanto el prompt como la inicialización del `MCPServerStreamableHttp` si se requieren parámetros nuevos.

Licencia

Consulte la raíz del repositorio para la licencia principal.

Contacto

Si necesitas ayuda para levantar el agente o integrarlo con `mcp_vcn`, deja un issue en el repositorio.

