# VuelaConNosotros — Chatbot de asistencia a pasajeros

Bienvenido: este repositorio contiene una propuesta de demostración para un agente conversacional que ayuda a pasajeros cuando hay incidencias (por ejemplo cancelaciones de vuelo). El proyecto está dividido en tres componentes principales:

- `mcp_vcn/` — Servicio MCP (herramientas) que expone operaciones sobre vuelos y reservas.
- `agente_vcn/` — El agente conversacional que usa las herramientas MCP y mantiene estado multi‑turno.
- `interfaz/` — Demo en Streamlit que actúa como interfaz de usuario y consume el endpoint del agente.

Objetivos clave:
- El agente puede iniciar conversaciones y manejar multi‑turno.
- Usa herramientas (mock / simulado) para consultar y modificar un "modelo" de base de datos de aerolínea.
- Diseñado para ser desplegable con Docker Compose para pruebas y demos rápidas.

Arquitectura

La comunicación entre componentes se realiza por HTTP dentro de la red de Docker Compose. En local (o en Docker Compose) los servicios se exponen en los puertos:

- `mcp_vcn`: puerto 8000 (MCP HTTP server)
- `agente_vcn`: puerto 8001 (API FastAPI con /chat)
- `interfaz`: porta 8501 (Streamlit UI)

## Diagrama de arquitectura

![Diagrama de arquitectura](img/arquitectura.png)

### Variables de entorno importantes

Para facilitar el despliegue se usa un archivo `.env` en la raíz del proyecto (no lo incluyas en control de versiones con secretos reales). Las variables que utiliza el compose y los servicios son, entre otras:

- `OPENAI_API_KEY` — clave de OpenAI (si el agente la utiliza para razonamiento). Selección interna del modelo está en el código.
- `URL_MCP` — URL pública del servicio MCP que usará el agente (p. ej. `http://mcp_vcn:8000/mcp`).
- `URL_CHAT` — URL del endpoint del agente que consume la interfaz (p. ej. `http://agente_vcn:8001/chat`).

He añadido un archivo ejemplo `.env.example` en la raíz con valores por defecto.

Cómo ejecutar (rápido)

1) Crear un archivo `.env` en la raíz (puedes copiar `.env.example`):

	- `.env` (ejemplo mínimo):

	  OPENAI_API_KEY=tu_api_key_aqui
	  URL_MCP=http://mcp_vcn:8000/mcp
	  URL_CHAT=http://agente_vcn:8001/chat

2) Levantar todos los servicios con Docker Compose:

	- Construir y ejecutar en segundo plano:

	  docker-compose up --build -d

	- Ver logs (ejemplo):

	  docker-compose logs -f agente_vcn

3) Abrir la interfaz Streamlit en el navegador:

	- http://localhost:8501

4) Probar el endpoint del agente (opcional):

	- Petición POST a `http://localhost:8001/chat` con JSON {"message": "Hola"}

Notas por servicio

- mcp_vcn: expone herramientas MCP (consultas y reservas). Está pensado como un servicio "mock" que usa utilidades locales y una base de datos simulada.
- agente_vcn: instancia un Agent y, en startup, conecta un cliente HTTP al MCP (`URL_MCP`). Expone `/chat` que devuelve un resumen con `output` y metadatos.
- interfaz: demo en Streamlit. Por defecto busca `CHAT_URL` o `URL_CHAT` en el entorno. Envía {"message": ...} al endpoint y muestra sólo el campo `output` al usuario.

Consejos y buenas prácticas

- No pongas claves reales en el repo. Usa `.env` local (o secretos en tu entorno de despliegue).
- Si quieres iterar en un servicio sin reconstruir todo, entra en la carpeta del servicio y ejecuta localmente (por ejemplo crear un virtualenv e instalar dependencias desde `pyproject.toml`).
- `docker-compose` usa nombres de servicio como hostname dentro de la red (por ej. `mcp_vcn`), por eso en `.env` usamos `http://mcp_vcn:8000/mcp`.

Problemas comunes y cómo depurarlos

- El agente devuelve 503: revisa logs del contenedor `agente_vcn` y asegúrate de que `mcp_vcn` está en marcha y accesible.
- Streamlit no llega a conectarse: verifica que `URL_CHAT` apunte al endpoint correcto (desde dentro del contenedor `interfaz` debe resolver `agente_vcn`).
- Errores relacionados con claves de OpenAI: asegúrate de que `OPENAI_API_KEY` está en el `.env` y accesible para el contenedor del agente.

Extensiones y siguientes pasos (sugerencias)

- Añadir tests automáticos para las herramientas MCP y para el endpoint `/chat`.
- Añadir un script de inicialización de datos (p. ej. poblar la BD mock) y documentarlo.
- Implementar healthchecks y dependencias en `docker-compose` para esperar readiness antes de exponer el servicio.

Contacto y licencia

Este repositorio es una demo; la licencia está en `LICENSE`. 



