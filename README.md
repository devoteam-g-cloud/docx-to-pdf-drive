# Transform local Docx to PDF using Google Drive

## why?

Because we did not find an easy way to transform .docx files to PDF in Python. So we did a script to import .docx file to Google Drive, transform it into a Google Doc, and download it as a PDF.

## setup

```
gcloud auth application-default login --scopes=https://www.googleapis.com/auth/drive.file
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## run

Copy your .docx file in the repo and change the name line 25, then

```
python main.py
```
