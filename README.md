# chatbot-vuela-con-nosotros

**Reto:** agente que inicia la conversación ante cancelación de vuelo, maneja estado multi‑turno, usa herramientas (mock), es resiliente a interrupciones y es escalable. 

**Stack propuesto orientado a ejecución rápida:**  Python + OpenAI SDK (razonamiento) + FastAPI (servicios) + FastMCP (herramientas) + Streamlit (UI) + Docker Compose (despliegue). Se hace mocks de la conexión a base de datos (simular interacción con base de datos de aerolinea)

Streamlit funcionará como demo para la parte frontend.
la propuesta aqui desarrollada es para la seccion de IA. En especifico la mostrada en MCP y Agentes.

Estas dos areas estan pensadas para ser resilientes y escalables

![Arquitectura del sistema](img/arquitectura.png)



