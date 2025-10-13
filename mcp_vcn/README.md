 # MCP Vuela Con Nosotros

 Este directorio contiene un microservicio MCP (Model Context Protocol) para consultar y gestionar vuelos y reservas. Está pensado para usarse como un componente independiente que expone herramientas (tools) mediante la librería `fastmcp`.

 ## Contenido

 - `main.py` — Define las herramientas MCP expuestas: `estado_vuelo`, `opciones_vuelo`, `reservar_vuelo` y `eliminar_reserva_vuelo`. Al ejecutarse en modo script inicia el servidor HTTP en el puerto 8000.
 - `utilidades.py` — Funciones de apoyo que gestionan la base de datos SQLite: conexión, creación/inicialización desde `inicial.sql`, consultas y operaciones de reserva.
 - `sbx.py` — Script de ejemplo que actúa como cliente MCP y muestra cómo llamar a las herramientas `estado_vuelo` y `opciones_vuelo` de forma asíncrona.
 - `inicial.sql` — Script SQL que crea las tablas `estado_vuelos` y `reservas` y carga datos de ejemplo.
 - `pyproject.toml` — Metadatos del paquete y dependencia mínima: `fastmcp>=2.12.4`.
 - `Dockerfile` — Imagen ligera para ejecutar el servicio usando la herramienta `uv`.
 - `vuelos.db` — (opcional) Base de datos SQLite ya creada; si no existe, `conectar_base_datos` la crea usando `inicial.sql`.

 ## Qué hace el servicio

 El servicio ofrece cuatro herramientas principales (MCP tools):

 - `estado_vuelo(vuelo: str)` — Devuelve la información del vuelo (estado, origen, destino, fecha, hora) para un número de vuelo.
 - `opciones_vuelo(origen: str, destino: str, fecha: str)` — Lista vuelos en la fecha indicada y calcula el primer asiento disponible en el rango 1..20 (o `null` si están todos ocupados).
 - `reservar_vuelo(vuelo: str, numero_asiento: int, id_pasajero: str)` — Intenta reservar un asiento y devuelve el resultado o un error si está ocupado.
 - `eliminar_reserva_vuelo(vuelo: str, numero_asiento: int, id_pasajero: str)` — Elimina una reserva existente.

 Todas las herramientas abren una conexión SQLite local usando `utilidades.conectar_base_datos()` y devuelven diccionarios con los datos o con la clave `error` en caso de excepción.

 ## Diagrama de componentes (Mermaid)

```mermaid
flowchart LR
  A[Cliente MCP - sbx.py]
  B[Servicio MCP - main.py]
  C[FastMCP - HTTP transport]
  D[SQLite DB - vuelos.db]
  E[inicial.sql]

  A -->|HTTP / mcp API| C
  C --> B
  B -->|conectar_base_datos()| D
  subgraph DBInit[Inicialización]
    E --> D
  end

  style DBInit fill:#f9f,stroke:#333,stroke-width:1px
```

 El diagrama muestra: el cliente (`sbx.py`) llama al endpoint MCP sobre HTTP; `main.py` recibe las llamadas y usa `utilidades.py` para acceder a la base de datos SQLite. Si `vuelos.db` no existe se ejecuta el script `inicial.sql` para poblarla.

 ## Ejecutar el componente de forma aislada (sin considerar el resto del repo)

 Las instrucciones están pensadas para un entorno local con Python 3.12 (el `pyproject.toml` indica >=3.12). Se describen dos formas: local (virtualenv) y Docker.

 Requisitos previos:

 - Python 3.12 instalado
 - (opcional) Docker si desea usar el contenedor

 ### Opción A — Ejecutar localmente (virtualenv)

 1. Abrir una terminal en la carpeta `mcp_vcn`.

2. Instalar `uv`

3. Sincronizar dependencias (desde `pyproject.toml`) y ejecutar el servicio con `uv`:

```powershell
# sincroniza las dependencias declaradas (crea un entorno aislado gestionado por uv)
uv sync --frozen --no-dev

# ejecutar el main.py usando el entorno sincronizado
uv run python main.py
```

El servicio debería quedar escuchando por defecto en http://localhost:8000/mcp

 4. Probar con el cliente de ejemplo (en otra terminal con el entorno activado):

 ```powershell
 uv run python sbx.py
 ```

 5. Alternativamente, usar curl para llamar a una herramienta (ejemplo `estado_vuelo`):

 ```powershell
 # Petición POST al endpoint /mcp/call (dependiendo de fastmcp internals)
 curl -X POST http://localhost:8000/mcp/call -H "Content-Type: application/json" -d '{"name":"estado_vuelo","args":{"vuelo":"PSO-ASU-101"}}'
 ```

 Si el servicio no arranca con `python main.py`, probablemente falte la dependencia `fastmcp` o `uv`. Instala `fastmcp` y, opcionalmente, `uv`:

 ```powershell
 pip install fastmcp uv
 # o
 pip install fastmcp
 ```

 ### Opción B — Ejecutar con Docker (aislado)

 1. Construir la imagen desde la carpeta `mcp_vcn` (desde PowerShell):

 ```powershell
 docker build -t mcp_vcn:latest .
 ```

 2. Ejecutar el contenedor exponiendo el puerto 8000:

 ```powershell
 docker run --rm -p 8000:8000 -v ${PWD}:/app mcp_vcn:latest
 ```

 Esto usará el `Dockerfile` incluido que instala dependencias con `uv sync` y ejecuta `uv run python main.py`.

 ### Observaciones y consejos

 - La base de datos SQLite se crea automáticamente si no existe, usando `inicial.sql`. Si desea partir de cero, elimine `vuelos.db` antes de iniciar el servicio.
 - `inicial.sql` ya incluye datos de ejemplo para varios vuelos y reservas. Ajuste las fechas si las pruebas requieren cambios.
 - Los puertos y el comportamiento por defecto pueden cambiar según versiones de `fastmcp` o `uv`.

 ## API rápida y ejemplos

 - Llamada a `estado_vuelo` (ejemplo):

 ```python
 from fastmcp import Client
 import asyncio

 client = Client("http://localhost:8000/mcp")

 async def run():
		 async with client:
				 res = await client.call_tool("estado_vuelo", {"vuelo": "PSO-ASU-101"})
				 print(res)

 asyncio.run(run())
 ```

 - Reservar un asiento (ejemplo):

 ```python
 from fastmcp import Client
 import asyncio

 client = Client("http://localhost:8000/mcp")

 async def reservar():
		 async with client:
				 res = await client.call_tool("reservar_vuelo", {"vuelo":"PSO-ASU-101","numero_asiento":2,"id_pasajero":"PAX999"})
				 print(res)

 asyncio.run(reservar())
 ```



 ## Licencia y créditos

 Consulta la raíz del repositorio para la licencia principal.
