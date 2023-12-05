from django.shortcuts import HttpResponse
from django.views import View
import os
import io
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaIoBaseDownload
import PyPDF2
from datetime import datetime
from store.models.customer import Users
from store.models.location import Location


class Google(View):
    def get(self, request):
        print("hitesh")
        google_drive_data = GoogleDrive()
        response = HttpResponse(google_drive_data)
        return response

def GoogleDrive():
    # The file that contains the OAuth 2.0 credentials.
    CLIENT_SECRET_FILE = 'store/Views/GoogleDriveAPI.json'

    # The name of the API and version of the api and
    API_NAME = 'drive'
    API_VERSION = 'v3'

    # The scopes that are required to access the API.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def create_service():
        # Create the credentials.
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If the credentials don't exist or are invalid, then create new ones.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Create the flow object.
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)

                # Run the flow to obtain the credentials.
                creds = flow.run_local_server(port=0)

                # Save the credentials for future use.
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
        # Create the service object.
        service = build(API_NAME, API_VERSION, credentials=creds)
        return service

    folder_id = '1riQFf7L2tvxNPEGZflh5Ami4r-ISgeTK'
    service = create_service()

    existing_patient_ids = set(Users.objects.values_list('patient_id', flat=True))
    fetch_patient_data_from_folder(service, folder_id, existing_patient_ids)


def fetch_patient_data_from_folder(service, folder_id, existing_patient_ids):
    stack = [(folder_id, None)]
    patient_data_by_date = {}

    while stack:
        current_folder_id, current_location_id = stack.pop()
        query = f"'{current_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
        subfolders = service.files().list(q=query).execute()

        for subfolder in subfolders.get('files', []):
            subfolder_id = subfolder['id']
            subfolder_name = subfolder['name']

            # Process the subfolder even if it's not a known location
            stack.append((subfolder_id, subfolder_name))
            technician_name = subfolder_name
            location_id = None

            if technician_name:
                location = Location.objects.filter(technician_name=technician_name).first()
                if location:
                    location_id = location.id

                query = f"'{subfolder_id}' in parents"
                subfolder_files = service.files().list(q=query).execute().get('files', [])

                for data in subfolder_files:
                    if data['mimeType'] == 'application/pdf':
                        file_id = data['id']
                        # Download the file content from Google Drive.
                        request = service.files().get_media(fileId=file_id)
                        pdf_files = io.BytesIO()
                        downloader = MediaIoBaseDownload(pdf_files, request)
                        done = False
                        while not done:
                            status, done = downloader.next_chunk()
                        pdf_reader = PyPDF2.PdfReader(pdf_files)

                        for page in pdf_reader.pages:
                            first_page_text = page.extract_text()
                            patient_id = str(first_page_text).split("Id :")[1].split(" ")[1].split("\n")[0]
                            if patient_id not in existing_patient_ids:
                                patient_name = str(first_page_text).split("Name :")[1].split("Age :")[0].split('\n')[0].strip()
                                patient_age = str(first_page_text).split("Age :")[1].split(" ")[1].split("\n")[0].strip()
                                if patient_age == "":
                                    age = 0
                                else:
                                    age = patient_age

                                gender = str(first_page_text).split("Gender :")[1].split("\n")[0].strip()
                                raw_date = str(first_page_text).split("Acquired on:")[1][0:11].strip()
                                formatted_date = datetime.strptime(raw_date, '%Y-%m-%d').date()

                                print(patient_name, age, gender, formatted_date)

                                # Update location_id within this loop if location is found
                                if formatted_date not in patient_data_by_date:
                                    patient_data_by_date[formatted_date] = []
                                patient_data_by_date[formatted_date].append(
                                    (patient_id, patient_name, age, gender))

                                location_instance = Location.objects.get(pk=location_id)

                                users = Users(
                                    patient_id=patient_id,
                                    patient_name=patient_name,
                                    age=age,
                                    gender=gender,
                                    date_field= formatted_date,
                                    phone = 18002702900,
                                    email = 'info@xraidigital.com',
                                    weight = 80,
                                    location = location_instance
                                )
                                users.save()
                                print(f"Patient saved: {users}")