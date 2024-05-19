#!/usr/bin/env python3

"""
pdf_parser.py
---------

Parses the pdf file and extracts the table from the mentioned page based on search criteria

Functions:
- extract_table_from_pdf: Brief description of what the function does.

Usage example:
    result = function_name(args)
    print(result)
"""

import pdfplumber
import pandas as pd

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
                raise ValueError(f"Table index {table_index} is out of range. Found {len(tables)} tables.")

        # If search_text is provided, find the table containing the text
        if search_text is not None:
            for table in tables:
                for row in table:
                    if any(search_text in cell for cell in row):
                        return table

            raise ValueError(f"No table containing text '{search_text}' found on page {page_number}.")

        # If neither table_index nor search_text is provided, return the first table
        return tables[0]


def pdf_parser():
    pdf_path = 'financials.pdf'
    password = 'APAPH5120F'
    page_number = 3
    table_index = None  # Change to specific index if needed
    search_text = 'Asset Class'  # Change to specific text if needed

    table = extract_table_from_pdf(pdf_path, password, page_number, table_index, search_text)

    # Convert to pandas DataFrame
    df = pd.DataFrame(table[1:], columns=table[0])  # Assuming the first row is the header
    print(df)
