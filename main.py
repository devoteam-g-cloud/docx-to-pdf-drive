import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
import shutil

# need to init using this : 
# gcloud auth application-default login --scopes=https://www.googleapis.com/auth/drive.file 
creds, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/drive"], quota_project_id="PROJECT_ID"
)

try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    # init google drive metadata
    file_metadata = {
        "name": "data.docx", # name of the file in Drive
        "parents": ["1gTqGY1LGj0nccSpO8DqjamTh2py_NDWJ"], # where to put the file
        "mimeType": "application/vnd.google-apps.document", # Google Doc mimetype to download it after
    }
    # create file object to be uploaded
    media = MediaFileUpload(
        "data.docx", # path to the file
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document", # .docx mimetype
    )
    # add file to Google Drive
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    # init request to download as pdf
    request = service.files().export(fileId=file.get("id"), mimeType="application/pdf")
    # init file reader
    fh = io.BytesIO()
    # init file downloader
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    # download chunks while they exists
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%" % int(status.progress() * 100))
    # reset file reader
    fh.seek(0)
    # save file localy
    with open("your_filename.pdf", "wb") as f:
        shutil.copyfileobj(fh, f)
except HttpError as error:
    print(f"An error occurred: {error}")
    file = None
