#!/usr/bin/env python3

"""
main.py
---------

Parses the pdf file and extracts the table from the mentioned page based on search criteria

Functions:
- main: Brief description of what the function does.
"""

from stocks import pdf_parser
from stocks import gmail_api as ga

def main():
    """
    Main metho. Starting point of the application

    Parameters:
    NONE

    Returns:
    type: Description of the return value.
    """
    service = ga.authenticate()

    # CDSL statement
    subject = 'CDSL Consolidated Account Statement (CAS)'
    msg = ga.search_email_by_subject(service, subject)
    if msg:
        ga.download_attachments(service, msg)

    # NPS statement
    subject = 'CDSL Consolidated Account Statement (CAS)'
    msg = ga.search_email_by_subject(service, subject)
    if msg:
        ga.download_attachments(service, msg)


if __name__ == '__main__' :
    main()
