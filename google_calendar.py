import os
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Alcance necesario para acceder al calendario
SCOPES = ['https://www.googleapis.com/auth/calendar']

def download_credentials():
    """Descarga el archivo credentials.json desde Google Cloud Storage."""
    credentials_url = os.getenv('GOOGLE_CALENDAR_CREDENTIALS_PATH')
    if not credentials_url:
        raise ValueError("La variable de entorno GOOGLE_CALENDAR_CREDENTIALS_PATH no está configurada.")
    
    response = requests.get(credentials_url)
    if response.status_code == 200:
        with open('credentials.json', 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"No se pudo descargar el archivo credentials.json. Código de estado: {response.status_code}")

def get_calendar_service():
    creds = None
    # Verifica si ya existe un token guardado
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si no hay credenciales válidas, inicia el flujo de autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Descargar el archivo credentials.json
            download_credentials()
            credentials_path = 'credentials.json'
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Guarda las credenciales para la próxima vez
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(summary, start_time, end_time):
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Europe/Madrid',
        },
    }
    calendar_id = '3acc61c8b27f26e8276ac2fae281794cbb07aef6de25b5d02d9b7408fbd1fc8a@group.calendar.google.com'
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event.get('htmlLink')