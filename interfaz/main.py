import os
import streamlit as st
import requests
import json


st.set_page_config(page_title="Chat - VuelaConNosotros", page_icon="✈️")

st.title("Asistente VuelaConNosotros — Chat")

# Config: prefer environment variable, then streamlit secrets (safely), then fallback
DEFAULT_CHAT_URL = os.environ.get("CHAT_URL")
if not DEFAULT_CHAT_URL:
	try:
		# st.secrets may raise StreamlitSecretNotFoundError if no secrets.toml exists
		DEFAULT_CHAT_URL = st.secrets.get("CHAT_URL")
	except Exception:
		DEFAULT_CHAT_URL = None

if not DEFAULT_CHAT_URL:
	DEFAULT_CHAT_URL = "http://localhost:8001/chat"

with st.sidebar:
	st.header("Configuración")
	chat_url = st.text_input("URL del endpoint /chat", value=DEFAULT_CHAT_URL)
	st.markdown("La app enviará POST JSON con {'message': 'tu mensaje'} al endpoint especificado.")


if "history" not in st.session_state:
	st.session_state.history = []  # list of tuples (user, assistant)


def send_message(message: str) -> str:
	"""Send a message to the agent endpoint and return the assistant 'output' text.

	If the response does not include 'output' or something fails, return a helpful error string.
	"""
	try:
		payload = {"message": message}
		headers = {"accept": "application/json", "Content-Type": "application/json"}
		resp = requests.post(chat_url, headers=headers, data=json.dumps(payload), timeout=15)
	except Exception as e:
		return f"ERROR: no se pudo conectar al endpoint ({e})"

	if resp.status_code != 200:
		# Try to include body when available
		body = resp.text
		return f"ERROR: endpoint devolvió código {resp.status_code}: {body}"

	try:
		data = resp.json()
	except Exception as e:
		return f"ERROR: respuesta no JSON ({e})\n{resp.text}"

	# The user must only see the 'output' field according to spec
	output = data.get("output")
	if output is None:
		# If output missing, try to extract a reasonable fallback from raw_responses
		raw = data.get("raw_responses")
		if raw and isinstance(raw, list):
			# try to find the last message-like output text
			for rr in reversed(raw):
				out = rr.get("output")
				if isinstance(out, list):
					for item in reversed(out):
						# item might be a dict containing 'content' with text
						if isinstance(item, dict):
							# For message items
							if item.get("type") == "message":
								content = item.get("content")
								if isinstance(content, list) and len(content) > 0:
									first = content[0]
									text = first.get("text") or first.get("output_text") or first.get("text")
									if text:
										return text
							# For function call outputs or other structures, try stringifying
							if "text" in item:
								return str(item.get("text"))
						# if out is a string
						if isinstance(out, str):
							return out
		return "ERROR: la respuesta no contiene el campo 'output'"

	# If output is not a string, stringify reasonable structures
	if isinstance(output, str):
		return output
	try:
		return json.dumps(output, ensure_ascii=False, indent=None)
	except Exception:
		return str(output)


def on_send() -> None:
	"""Callback for the Enviar button: reads `st.session_state['input']`, sends it,
	appends to history and clears the input safely from within the callback."""
	user_msg = st.session_state.get("input", "").strip()
	if not user_msg:
		return
	# append placeholder while waiting
	st.session_state.history.append((user_msg, "..."))
	# send to server
	assistant_text = send_message(user_msg)
	# replace the last history item placeholder
	st.session_state.history[-1] = (user_msg, assistant_text)
	# clear input safely inside callback
	st.session_state["input"] = ""


st.subheader("Chat")

col1, col2 = st.columns([4, 1])

with col1:
	st.text_area("Escribe tu mensaje", height=120, key="input")
with col2:
	st.button("Enviar", on_click=on_send)

# Render history
for user_msg, assistant_msg in st.session_state.history:
	st.markdown(f"**Tú:** {user_msg}")
	# Only show assistant 'output' text
	st.markdown(f"**Asistente:** {assistant_msg}")

st.markdown("---")
st.caption("Solo se muestra al usuario el campo 'output' de la respuesta del agente.")

