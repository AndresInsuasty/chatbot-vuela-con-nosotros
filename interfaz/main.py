"""Simple Streamlit chat interface for VuelaConNosotros agent."""
import os
import json
import streamlit as st
import requests
import time


st.set_page_config(page_title="Chat - VuelaConNosotros", page_icon="✈️")

st.title("Asistente VuelaConNosotros — Chat")

DEFAULT_CHAT_URL = os.environ.get("CHAT_URL")
if not DEFAULT_CHAT_URL:
    try:
        DEFAULT_CHAT_URL = st.secrets.get("CHAT_URL")
    except Exception:
        DEFAULT_CHAT_URL = None

if not DEFAULT_CHAT_URL:
    DEFAULT_CHAT_URL = os.getenv("URL_CHAT", "http://localhost:8001/chat")

with st.sidebar:
    st.header("Configuración")
    chat_url = st.text_input("URL del endpoint /chat", value=DEFAULT_CHAT_URL)
    st.markdown(
        "La app enviará POST JSON con {'message': 'tu mensaje'} al endpoint especificado."
    )


if "history" not in st.session_state:
    st.session_state.history = []  # list of tuples (user, assistant)


def send_message(message: str) -> str:
    """Send a message to the agent endpoint and return the assistant 'output' text.

    If the response does not include 'output' or something fails, return a helpful error string.
    """
    try:
        payload = {"message": message}
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        resp = requests.post(
            chat_url, headers=headers, data=json.dumps(payload), timeout=15
        )
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
                                    text = (
                                        first.get("text")
                                        or first.get("output_text")
                                        or first.get("text")
                                    )
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


# migrate old history to messages if present
if "messages" not in st.session_state:
    # Convert from older `history` format if available
    if "history" in st.session_state and isinstance(st.session_state.history, list):
        st.session_state.messages = []
        for user_msg, assistant_msg in st.session_state.history:
            st.session_state.messages.append({"role": "user", "content": user_msg})
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_msg}
            )
    else:
        st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input using chat_input
prompt = st.chat_input("Escribe tu mensaje...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    assistant_text = send_message(prompt)

    # Stream the assistant response into the chat
    def response_generator(text: str):
        """Yield text one word at a time with a slight delay to simulate streaming.
        
        Args:
			text (str): The full text to stream.
		Yields:
			str: The next word with a trailing space.
		"""
        
        for word in str(text).split():
            yield word + " "
            time.sleep(0.02)

    with st.chat_message("assistant"):
        # Use write_stream to render the streaming response
        try:
            response = st.write_stream(response_generator(assistant_text))
        except Exception:
            # Fallback: just write the full text
            st.markdown(assistant_text)
            response = assistant_text

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})

st.markdown("---")
st.caption("Solo se muestra al usuario el campo 'output' de la respuesta del agente.")
