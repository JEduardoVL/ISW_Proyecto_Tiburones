import os
import tempfile
import time
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

def authenticate():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    creds_path = os.path.join(base_dir, 'service_account.json')
    with open(creds_path, 'r') as f:
        creds_json = json.load(f)
    creds = service_account.Credentials.from_service_account_info(creds_json, scopes=['https://www.googleapis.com/auth/drive'])
    return creds

def upload_pdf(file):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': file.name, 
        'parents': ['1v-RNvA4ioDpRNmmZ1DVqEdsFsEzl9_Sd']  # Modifica con tu carpeta específica
    }

    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_content = file.read()
            temp_file.write(file_content)
            temp_file.flush()
            temp_file.close()

            media = MediaFileUpload(temp_file.name, mimetype='application/pdf')
            file_resource = service.files().create(
                body=file_metadata, media_body=media, fields='id, webViewLink'
            ).execute()

        # Pequeña pausa para asegurar que el archivo no esté bloqueado
        time.sleep(1)
    finally:
        try:
            os.unlink(temp_file.name)
        except PermissionError as e:
            print(f"No se pudo eliminar el archivo temporal: {e}")

    # Hacer que el archivo sea público
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(
        fileId=file_resource['id'], body=permission
    ).execute()

    return file_resource['webViewLink']
