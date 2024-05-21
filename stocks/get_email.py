#!/usr/bin/env python3

"""
get_email.py
---------

Parses the pdf file and extracts the table from the mentioned page based on search criteria

Functions:
- authenticate: Google api authentication
- extract_table_from_pdf: Brief description of what the function does.

"""

import base64
import pdfplumber

def search_email(service, sender=None, subject=None):
    """
    Brief description of the function's purpose.

    Parameters:
    param1 (type): Description of the first parameter.
    param2 (type): Description of the second parameter.

    Returns:
    type: Description of the return value.
    """
    try:
        # Construct the query string
        query = ''
        if sender:
            query += f'from:{sender} '
        if subject:
            query += f'subject:{subject}'

        # Search for emails with the specified query
        results = service.users().messages().list(userId='me', q=query.strip()).execute()
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
        sender = next((header['value'] for header in headers if header['name'] == 'From'), None)
        print(f"Subject: {subject}")
        print(f"From: {sender}")
        return msg

    except Exception as error:
        print(f'An error occurred: {error}')
        return None


def download_attachments(service, msg):
    """
    Brief description of the function's purpose.

    Parameters:
    param1 (type): Description of the first parameter.
    param2 (type): Description of the second parameter.

    Returns:
    type: Description of the return value.
    """
    try:
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['filename']:
                    if 'data' in part['body']:
                        data = part['body']['data']
                    else:
                        att_id = part['body']['attachmentId']
                        att = service.users().messages().attachments().get(
                            userId='me', messageId=msg['id'], id=att_id).execute()
                        data = att['data']
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = part['filename']

                    with open(path, 'wb') as f:
                        f.write(file_data)
                    print(f'Attachment {part["filename"]} downloaded.')
                    return part["filename"]

    except Exception as error:
        print(f'An error occurred while downloading attachments: {error}')


def extract_table_from_pdf(pdf_path, password, page_number, table_index=None, search_text=None):
    """
    Brief description of the function's purpose.

    Parameters:
    param1 (type): Description of the first parameter.
    param2 (type): Description of the second parameter.

    Returns:
    type: Description of the return value.
    """
    with pdfplumber.open(pdf_path, password=password) as pdf:
        page = pdf.pages[page_number - 1]  # pages are 0-indexed
        tables = page.extract_tables()

        if not tables:
            raise ValueError(f"No tables found on page {page_number}.")

        # If table_index is provided, return that table
        if table_index is not None:
            if table_index < len(tables):
                return tables[table_index]
            else:
                raise ValueError(f"Table index {table_index} is out of range."
                                 + f"Found {len(tables)} tables.")

        # If search_text is provided, find the table containing the text
        if search_text is not None:
            for table in tables:
                for row in table:
                    if any(search_text in cell for cell in row):
                        return table

            raise ValueError(f"No table containing text '{search_text}'"
                             + f"found on page {page_number}.")

        # If neither table_index nor search_text is provided, return the first table
        return tables[0]
