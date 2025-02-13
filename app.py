from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Obtener variables de entorno
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID')

@app.route('/')
def index():
    # Servir el archivo index.html desde la raíz
    with open('index.html', 'r', encoding='utf-8') as file:
        return file.read()

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    summary = data.get('summary')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not all([summary, start_time, end_time]):
        return jsonify({"status": "error", "message": "Faltan datos para agendar la cita."}), 400

    try:
        # Crear el evento en Google Calendar
        event_link = create_event(summary, start_time, end_time)
        return jsonify({
            "status": "success",
            "message": "Cita agendada exitosamente.",
            "event_link": event_link,
            "follow_up": "¿Ha entendido mi respuesta? ¿Desea confirmar algo más?"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def create_event(summary, start_time, end_time):
    # Aquí deberías implementar la lógica para crear un evento en Google Calendar
    # Por ahora, devolveremos un enlace de evento ficticio
    return "https://calendar.google.com/event?eid=ficticio"

if __name__ == '__main__':
    app.run(debug=True)