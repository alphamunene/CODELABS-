from __future__ import print_function
import os
import pickle
import io
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """Shows basic usage of the Drive v3 API.
    Lists the names and ids of the first 10 files the user has access to.
    """
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file(file_path, mime_type='application/octet-stream'):
    service = authenticate_google_drive()
    
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype=mime_type)

    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print(f'File ID: {file.get("id")}')

if __name__ == '__main__':
    # List of files to upload
    files_to_upload = [
        'output_files/shuffled_data.json',
        'output_files/shuffled_data.jsonl',
        'output_files/similarities.json',
        'output_files/special_char_names.txt'
    ]
    
    for file_path in files_to_upload:
        if os.path.exists(file_path):
            upload_file(file_path)
        else:
            print(f"File not found: {file_path}")
