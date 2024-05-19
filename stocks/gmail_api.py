#!/usr/bin/env python3


import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
      # Call the Gmail API
      service = build("gmail", "v1", credentials=creds)
      return service
    except HttpError as error:
      # TODO(developer) - Handle errors from gmail API.
      print(f"An error occurred: {error}")

def search_email_by_subject(service, subject):
    try:
        # Search for emails with the specified subject
        query = f'subject:{subject}'
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return

        # Get the first message that matches the query
        msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
        
        # Print message details
        print(f"Message snippet: {msg['snippet']}")
        
        # Get the email data (optional)
        payload = msg.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
        print(f"Subject: {subject}")
        return msg

    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def download_attachments(service, msg):
    try:
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['filename']:
                    if 'data' in part['body']:
                        data = part['body']['data']
                    else:
                        att_id = part['body']['attachmentId']
                        att = service.users().messages().attachments().get(userId='me', messageId=msg['id'], id=att_id).execute()
                        data = att['data']
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = part['filename']

                    with open(path, 'wb') as f:
                        f.write(file_data)
                    print(f'Attachment {part["filename"]} downloaded.')

    except Exception as error:
        print(f'An error occurred while downloading attachments: {error}')


def main():
    service = authenticate()
    subject = 'CDSL Consolidated Account Statement (CAS)'
    msg = search_email_by_subject(service, subject)
    if msg:
        download_attachments(service, msg)


if __name__ == "__main__":
    main()
