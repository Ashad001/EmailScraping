import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from CREDS import FOLDER_ID, FOLDER_KEY_FILE

def create_subfolder(service, parent_folder_id, subfolder_name):
    folder_metadata = {
        'name': subfolder_name,
        'parents': [parent_folder_id],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id')

def upload_csv_files(service, source_folder_path, destination_folder_id):
    files = [f for f in os.listdir(source_folder_path) if f.endswith('.csv') and os.path.isfile(os.path.join(source_folder_path, f))]
    
    for file_name in files:
        file_path = os.path.join(source_folder_path, file_name)

        # Extract the account name from the file name
        account_name = file_name.split('_')[0]

        # Check if the subfolder for the account exists, if not, create it
        subfolder_id = None
        query = f"name='{account_name}' and '{destination_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        existing_subfolders = service.files().list(q=query).execute().get('files', [])
        
        if not existing_subfolders:
            subfolder_id = create_subfolder(service, destination_folder_id, account_name)
        else:
            subfolder_id = existing_subfolders[0]['id']

        # Check if the file already exists in the subfolder
        query = f"name='{file_name}' and '{subfolder_id}' in parents and trashed=false"
        existing_files = service.files().list(q=query).execute().get('files', [])

        # Check if file is in existing files, if yes, continue to the next file...
        if file_name in [file['name'] for file in existing_files]:
            print(f"File already exists: {file_name}")
            continue

        media_body = MediaFileUpload(file_path, mimetype='application/vnd.ms-excel')
        file_metadata = {'name': file_name, 'parents': [subfolder_id]}

        try:
            service.files().create(body=file_metadata, media_body=media_body).execute()
            print(f"Uploaded: {file_name}")
        except HttpError as e:
            print(f"Error uploading {file_name}: {e}")

if __name__ == "__main__":
    scope = ["https://www.googleapis.com/auth/drive"]
    service_account_json_key = FOLDER_KEY_FILE
    folder_id = FOLDER_ID
    credentials = service_account.Credentials.from_service_account_file(
        filename=service_account_json_key, scopes=scope
    )
    service = build("drive", "v3", credentials=credentials)

    source_folder_path = "./valid_csvs"

    destination_folder_id = folder_id

    upload_csv_files(service, source_folder_path, destination_folder_id)
