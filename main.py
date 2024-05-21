#!/usr/bin/env python3

"""
main.py
---------

Parses the pdf file and extracts the table from the mentioned page based on search criteria

Functions:
- main: Brief description of what the function does.
"""
import pandas as pd
from stocks import get_email, gmail_api, graph_generation

def main():
    """
    Main metho. Starting point of the application

    Parameters:
    NONE

    Returns:
    type: Description of the return value.
    """
    service = gmail_api.authenticate()

    # CDSL statement
    subject = 'CDSL Consolidated Account Statement (CAS)'
    msg = get_email.search_email(service, subject)
    if msg:
        filename = get_email.download_attachments(service, msg)

    pdf_path = filename
    password = 'APAPH5120F'
    page_number = 3
    table_index = None  # Change to specific index if needed
    search_text = 'Asset Class'  # Change to specific text if needed

    table = get_email.extract_table_from_pdf(pdf_path, password, page_number, table_index, search_text)

    # Convert to pandas DataFrame
    df = pd.DataFrame(table[1:], columns=table[0])  # Assuming the first row is the header
    graph_generation.graph_generation(df)

    # NPS statement
    # subject = 'CDSL Consolidated Account Statement (CAS)'
    # sender = ''
    # msg = get_email.search_email(service, subject)
    # if msg:
    #     get_email.download_attachments(service, msg)


if __name__ == '__main__' :
    main()
