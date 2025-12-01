# main.py
from fastapi import FastAPI, Request
import requests # Para hablar con Meta

app = FastAPI()

# Tus credenciales de Meta Developers
TOKEN_META = "TU_ACCESS_TOKEN_LARGO"
PHONE_ID = "TU_PHONE_NUMBER_ID"
VERIFY_TOKEN = "UNA_CLAVE_QUE_TU_INVENTAS" # Ej: "búho_secreto_123"

# PASO 1: VERIFICACIÓN (Meta te preguntará si eres tú)
@app.get("/webhook")
async def verificar_webhook(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return int(challenge) # Le regresas el código para confirmar
    return "Error de autenticación"

# PASO 2: RECIBIR EL MENSAJE DEL USUARIO
@app.post("/webhook")
async def recibir_mensaje(request: Request):
    data = await request.json()
    
    try:
        # Navegamos el JSON complejo que manda WhatsApp
        mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]
        texto_usuario = mensaje['text']['body']
        numero_usuario = mensaje['from'] # El ID del usuario (su teléfono)

        print(f"Usuario {numero_usuario} dijo: {texto_usuario}")

        # --- AQUÍ CONECTAS TU LÓGICA ---
        # 1. Llamas a tu AI Agent (OpenAI)
        # 2. Guardas en tu Base de Datos
        # -------------------------------

        # Respondemos al usuario (opcional)
        enviar_respuesta(numero_usuario, "Recibido. Procesando en la app...")

    except KeyError:
        pass # A veces llegan notificaciones de estado, no mensajes
    
    return {"status": "ok"}

def enviar_respuesta(numero, texto):
    url = f"https://graph.facebook.com/v17.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN_META}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "text": {"body": texto}
    }
    requests.post(url, headers=headers, json=data)