from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()


agent = Agent(name="Assistant", instructions="Eres un asistente útil.")

result = Runner.run_sync(agent, "Escribe un haiku sobre la recursión en programación.")
print(result.final_output)

# Código dentro del código,
# Funciones que se llaman a sí mismas,
# El baile del bucle infinito.